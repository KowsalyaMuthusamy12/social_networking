from django.db import models
from django.contrib.auth import models as auth_models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not name:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            name=name        
        )       

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            name=name,
        )
        
        user.is_admin = True
        user.role = 1
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(max_length=255)
    last_login = models.DateTimeField(auto_now=True, null=False)
    created_on = models.DateTimeField(auto_now_add=True, null=False)
    updated_on = models.DateTimeField(auto_now=True, null=False)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        db_table='user'



class Friends(models.Model):
    requested_by= models.ForeignKey(User,on_delete=models.CASCADE,related_name='friend_req_by')
    requested_to= models.ForeignKey(User,on_delete=models.CASCADE,related_name='friend_req_to')
    status= models.CharField(max_length=100,null=False)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table='friends'