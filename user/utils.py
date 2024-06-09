import re

from user.models import User
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import AccessToken,RefreshToken

def is_valid_email(email):
    try:
        email_validate=re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        return True if re.fullmatch(email_validate, email) else False
    except Exception as e:
        return None
    
def auth_users(email,password):
    user =User.objects.get(email=email)
    if user:
        return check_password(password,user.password)
    
def auth_token(user):
    access = AccessToken.for_user(user)
    refresh=RefreshToken.for_user(user)

    return {"access_token": str(access),
    "refresh_token":str(refresh)}
