from operator import itemgetter

import pandas as pd
import re 
from langchain.chat_models import AzureChatOpenAI, ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableLambda, RunnableMap
from langchain.utilities import SQLDatabase


from taskweaver.plugin import Plugin, register_plugin


@register_plugin
class SqlPullMssqlData(Plugin):
    db = None

    def __call__(self, query: str):
        api_type = self.config.get("api_type", "azure")
        if api_type == "azure":
            model = AzureChatOpenAI(
                azure_endpoint=self.config.get("api_base"),
                openai_api_key=self.config.get("api_key"),
                openai_api_version=self.config.get("api_version"),
                azure_deployment=self.config.get("deployment_name"),
                temperature=0,
                verbose=True,
            )
        elif api_type == "openai":
            model = ChatOpenAI(
                openai_api_key=self.config.get("api_key"),
                model_name=self.config.get("deployment_name"),
                temperature=0,
                verbose=True,
            )
        else:
            raise ValueError("Invalid API type. Please check your config file.")

        template = """Based on the table schema below, write a SQL query that would answer the user's question:
            {schema}

            Question: {question}
            Please only write the sql query.
            Do not add any comments or extra text.
            Do not wrap the query in quotes or ```sql.
            SQL Query:"""
        prompt = ChatPromptTemplate.from_template(template)

        if self.db is None:
            # Create the connection URL for SQLAlchemy
            username = self.config.get("AZURE_DEV_SQL_USER")
            password = self.config.get("AZURE_DEV_SQL_PWD")
            server = self.config.get("AZURE_DEV_SQL_SERVER")
            database = self.config.get("AZURE_DEV_SQL_DB")
            connection_url = f'mssql+pymssql://{username}:{password}@{server}/{database}'
            # self.db = SQLDatabase.from_uri(self.config.get("sqlite_db_path"))
            self.db = SQLDatabase.from_uri(connection_url)

        def get_schema(_):
            print("Getting schema")
            print(self.db.get_table_info())
            return self.db.get_table_info()

        inputs = {
            "schema": RunnableLambda(get_schema),
            "question": itemgetter("question"),
        }
        sql_response = RunnableMap(inputs) | prompt | model.bind(stop=["\nSQLResult:"]) | StrOutputParser()

        sql = sql_response.invoke({"question": query})
        # print("LLM generated sql statement:\n")
        # print(sql)
        
        # SELECT * FROM INFORMATION_SCHEMA.TABLES. to show the tables in the db.
        allowed_key_words = ["SELECT", "select"]
        # allowed_key_words = ["NOTATALL"]
    
        # regex to match sql string beginning with select 
        if not any(re.match(rf'^\s*{word}', sql) for word in allowed_key_words):
            df = pd.DataFrame() 
            # what is the age of the youngest person in titanic table?
            # df = pd.DataFrame(["invalid sql statement", f"{type(sql)}", f"{repr(sql)}"])
            """
            The result of above Python code after execution is:
                                                            0
            0                           invalid sql statement
            1                                   <class 'str'>
            2  'SELECT MIN(Age) AS YoungestAge FROM titanic;'
            """
            return df, (
                    f"I have generated a SQL query based on `{query}`.\nThe SQL query is {sql}.\n" f"The generated SQL statement does not start with SELECT. Please try again."
            )
        
        else: 
            result = self.db._execute(sql, fetch="all")

            df = pd.DataFrame(result)

            if len(df) == 0:
                return df, (
                    f"I have generated a SQL query based on `{query}`.\nThe SQL query is {sql}.\n" f"The result is empty."
                )
            else:
                return df, (
                    f"I have generated a SQL query based on `{query}`.\nThe SQL query is {sql}.\n"
                    f"There are {len(df)} rows in the result.\n"
                    f"The first {min(5, len(df))} rows are:\n{df.head(min(5, len(df))).to_markdown()}"
                )