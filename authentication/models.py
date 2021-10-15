from django.conf import settings
from django.contrib.auth.models import ( AbstractBaseUser, BaseUserManager, PermissionsMixin )
from django.db import models



from django.db import models
import jwt
from datetime import datetime, timedelta

class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
    
        if username is None:
            raise TypeError('Users must have username')
        if email is None:
            raise TypeError("Users must have an email address.")
        
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        
        return user

    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError('SuperUsers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=100, unique=True)

    email = models.EmailField(db_index=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        template = '{0.id}'
        return template.format(self)

    @property
    def token(self):
        return self._generate_jwt_token()
    
    def get_full_name(self):
        return self.username
    
    def get_short_name(self):
        return self.username
    
    def _generate_jwt_token(self):
        dt  = datetime.now() + timedelta(seconds=86400)

        token = jwt.encode({
            'id': self.pk,
            'exp': dt.utcfromtimestamp(dt.timestamp()) 
        }, settings.SECRET_KEY, algorithm='HS256')
        
        # Last version used the code on the right to return a decoded token/ new update uses below code:     return token.decode('utf-8') 
        # jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"] )
        return token



   


