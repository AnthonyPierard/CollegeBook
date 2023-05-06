rm ./db.sqlite3
python ./manage.py makemigrations Account
python ./manage.py makemigrations Configuration
python ./manage.py makemigrations Event
python ./manage.py makemigrations Reservation
python ./manage.py migrate
python ./manage.py shell -c "from Account.models import User; User.objects.create_superuser('admin@admin.com', 'adminpassword')"
find -type d -name migrations -a -prune -exec rm -rf {} \;
find -type d -name __pycache__ -a -prune -exec rm -rf {} \;
rm -rf Event/static/json/*
rm -rf CollegeBook/Media/QR/*
rm -rf CollegeBook/Media/Ticket/*
find Configuration/static/json/ -type f -not -name "allSeat.json" -not -name "onlySeat.json" -not -name "onlyStanding.json" -not -name "standingWithBleacher.json" -delete