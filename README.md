# Sneaky

This is the final year project for IT Bachelor Degree in Greenwich Univerity.
All the copyrights are subjected as free license.

# Installation on Windows 10

* Step 1:
Download the project and unzip.

* Step 2:
Instal Python 3.7.4 64-bit: https://www.python.org/downloads/release/python-374/

* Step 3:
Install Pipenv:
2.1 - Run Windows Power Shell as Administrator.
2.2 - Run the following command in Power Shell: 'pip install pipenv'

* Step 4:
4.1 - Navigate to the project folder in the Windows Power Shell.
4.2 - Create virtual environment using Pipenv: 'pipenv shell'

* Step 5:
Make sure the virtual environment is activated
If not, activated in the project folder using this command in Powershell: 'pipenv shell'
Run the follwing command in Power Shell to install all packages in the Pipfile: 'pipenv sync'

* Step 6:
Navigate to the 'src' folder: 'cd src'

* Step 7:
Start the web server using this command: 'python manage.py runserver'
