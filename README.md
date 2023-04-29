# CollegeBook

## WINDOWS

To launch the project :
```bash

python -m venv env
./env/Scripts/activate
pip install -r requirements.txt
```
Then, run restore_BD.sh under 

## LINUX
To launch the project : 
```bash
python -m venv env
source ./env/bin/activate
pip install -r unix_requirements.txt
rm ./db.sqlite3
python ./manage.py makemigrations Account
python ./manage.py makemigrations Configuration
python ./manage.py makemigrations Event
python ./manage.py makemigrations Reservation
python ./manage.py migrate
python ./manage.py shell -c "from Account.models import User; User.objects.create_superuser('admin@admin.com', 'adminpassword')"
find -type d -name migrations -a -prune -exec rm -rf {} \;
find -type d -name __pycache__ -a -prune -exec rm -rf {} \;
```
