@echo OFF

set python_env="C:\Users\jorda\Documents\Python_Projects\automation\env\Scripts\activate"
set python_script="C:\Users\jorda\Documents\Python_Projects\automation\src\memberhip_articles.py"

echo Activating Python environment
call %python_env%
echo Scraping Membership Articles
py %python_script% %*

deactivate