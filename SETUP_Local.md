# Setup this taskweaver run

## Create venv on macosx
use a custom `create_env.sh` script to create a venv on macosx apple silicon

```powershell
cd $env:USERPROFILE\Documents\VCS\llm-train;

$VERSION="3.11";
$ENV_NAME="twagent";
$ENV_SURFIX="pip";
$PM="pip";
$WORK_DIR="$env:USERPROFILE\Documents\VENV\";
.\envtools\create_env.ps1 -VERSION $VERSION -ENV_NAME $ENV_NAME -ENV_SURFIX $ENV_SURFIX -PM $PM -WORK_DIR $WORK_DIR;
```

```powershell
$VERSION="3.11";
$ENV_NAME="twagent";
$ENV_SURFIX="pip";

$ENV_FULL_NAME = "$ENV_NAME$VERSION$ENV_SURFIX";
# with the closing "\"
$ENV_DIR="$env:USERPROFILE\Documents\VENV\";

# absolute path of requirements.txt to install for the python venv
$PROJ_DIR="$env:USERPROFILE\Documents\VCS\democollections\ai-analytics-agent";
$SubProj=""
# $SubProj="01-foundamentals\"
# $typeProj="_fdy"
$typeProj=""
$PackageFile="$PROJ_DIR\${SubProj}requirements${typeProj}.txt";

& "$ENV_DIR$ENV_FULL_NAME\Scripts\Activate.ps1";
Invoke-Expression "(Get-Command python).Source";

& "python" -m pip install --upgrade pip;
& "python" -m pip install -r $PackageFile --no-cache-dir;
```

<!--
```shell
VERSION=3.10;
PREFIX=twlc;
ENV_NAME="${PREFIX}${VERSION}";
source ~/VENV/${ENV_NAME}/bin/activate
python3 -m pip install --upgrade pip
# python3 -m pip install --no-cache-dir -r requirements_arm64_dev.txt
python3 -m pip install --no-cache-dir -r requirements_arm64_dev3.txt
# python3 -m pip install --no-cache-dir -r ../../requirements_arm64_dev.txt
```
-->

## edit the config to setup the azure open ai model backend

```shell
./project/taskweaver_config.json
```

## start the project from terminal
activate the python virtual environment

then
```shell
python -m taskweaver -p ./project/
```

## Start the experimental UI
```shell
cd <gitrepo_root>/playground/UI
chainlit run app.py
```

or
```shell
python -m chainlit run -h --host 0.0.0.0 --port 8181 ./playground/UI/app.py
cd playground/UI/ && python -m chainlit run -h --host 0.0.0.0 --port 8181 app.py
```

```shell
cd /app/playground/UI/ && python -m chainlit run -h --host 0.0.0.0 --port 8181 app.py

# python -m chainlit run --host 0.0.0.0 --port 8181 /app/playground/UI/app.py
```

## Run Locally on Windows Powershell
```powershell
cd ./playground/UI/ 
& "python" -m chainlit run -h --host 0.0.0.0 --port 8181 app.py

# python -m chainlit run --host 0.0.0.0 --port 8181 /app/playground/UI/app.py
```


## Remove branch
```shell
git branch -d <branch_local>
git push origin -d <branch_remolte>
```

In azure cloud shell
# https://learn.microsoft.com/en-us/cli/azure/acr?view=azure-cli-latest#az-acr-build

## Use TaskWeaver as a Library
* https://microsoft.github.io/TaskWeaver/docs/usage/library/


## Remove all package from venv
```shell
python3 -m pip freeze | xargs pip uninstall -y
python3 -m pip list
```


## Reference:
* Chainlit https://microsoft.github.io/TaskWeaver/docs/usage/webui/
* TaskWeaver Intro https://medium.com/microsoftazure/introducing-taskweaver-80f4ac6d0788
* TaskWeaver UI https://microsoft.github.io/TaskWeaver/docs/usage/webui