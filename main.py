import os
os.system("/opt/render/project/src/.venv/bin/python -m pip install --upgrade pip")
os.system("pip3 install -r requirements.txt")
os.system("python manage.py runserver")