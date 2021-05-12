pip install pipenv
mkdir .venv
if [[ ${build_env} != 'production' ]]; then
    pipenv install --dev #--skip-lock
else
    pipenv install #--skip-lock
fi