Ensure to do this things while setting up app:

1.
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

2.
Check if migrations are done right. Maybe you need to add migrations folder and __init_ _.py file inside it.

3.
Add permissions to group deafult and create other needed groups manualy.