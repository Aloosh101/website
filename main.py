import os
os.system("/opt/render/project/src/.venv/bin/python -m pip install --upgrade pip")
os.system("pip3 install -r requirements.txt")
os.system("pip3 install Django==4.1.3")
os.system("python manage.py runserver")
