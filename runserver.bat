@echo off
cd %~dp0
echo +-------------------------------------------------------+
echo  please input link
echo +-------------------------------------------------------+
set /P link=
cd .. & venv\Scripts\activate & cd Proj & python manage.py makemigrations & python manage.py migrate & start http://127.0.0.1:8000/%link% & python manage.py runserver