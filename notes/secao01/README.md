Aula 03 - Ambiente virtual

Criar ambiente virtual

$ virtualenv venv -p python3

Para ativar o ambiente:

$ source venv/bin/activate

Para desativar

$ deactivate

Aula 04 - Configurando o Django

$ source venv/bin/activate
$ cd src
$ pip install django==1.11.29 #Ultima release, sem suporte desde 2020
$ django-admin startproject simplemooc
$ python manage.py runserver
