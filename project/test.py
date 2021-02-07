import json

from django.contrib.auth.models import User

with open('C:\\Users\\Alexis\\CSnSW\\Projects\\YouTubeFeed\\sample.users.json', 'r') as json_file:
    users = json.load(json_file)

for user in users:
    print(user)
    User.objects.create_user(
        username=user.get('username'),
        password=user.get('password'),
        first_name=user.get('first_name'),
        last_name=user.get('last_name'),
        is_staff=user.get('is_staff'),
        is_superuser=user.get('is_superuser')
    )
