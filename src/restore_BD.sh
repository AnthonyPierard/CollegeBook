rm ./db.sqlite3
# find -type d -name migration -a -prune -exec rm -rf {} \;
py ./manage.py makemigrations Account
py ./manage.py makemigrations Configuration
py ./manage.py makemigrations Event
py ./manage.py makemigrations Reservation
py ./manage.py migrate
py ./manage.py shell -c "from Account.models import User; User.objects.create_superuser('admin@admin.com', 'adminpassword')"
find -type d -name migrations -a -prune -exec rm -rf {} \;
find -type d -name __pycache__ -a -prune -exec rm -rf {} \;