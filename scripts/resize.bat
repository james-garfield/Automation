@echo OFF

@REM Es un script para redimensionar una imagen

set python_env="C:\Users\jorda\Documents\Python_Projects\automation\env\Scripts\activate"
set python_script="C:\Users\jorda\Documents\Python_Projects\automation\src\file_resizer.py"

call %python_env%
py %python_script% %*

call deactivate