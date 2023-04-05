from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, phone, password=None):
        if not email:         
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            password=password,
            
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username,phone, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            phone=phone,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.role = 'admin'
        user.save(using=self._db)
        
        return user

class Account(AbstractBaseUser):

    # USER_USER='USER'
    # USER_EVENT_MANAGEMENT='EVENT_MANAGEMENT'
    
    # USER_CHOICES=[
    #     (USER_USER,'USER'),
    #     (USER_EVENT_MANAGEMENT,'EVENT_MANAGEMENT')

    # ]


    email = models.EmailField(verbose_name="email", max_length=60, unique=False)
    username = models.CharField(max_length=60, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False,null=True,blank=True)
    is_active = models.BooleanField(default=True,null=True,blank=True)
    is_staff = models.BooleanField(default=False,null=True,blank=True)
    is_superuser = models.BooleanField(default=False,null=True,blank=True)
    full_name = models.CharField(max_length=30,null=True,blank=True)
    phone = models.CharField(max_length=30,null=True,blank=True)
    address = models.CharField(max_length=140,null=True,blank=True)
    dob = models.CharField(max_length=30,null=True,blank=True)
    # role = models.CharField(max_length=30,null=True,blank=True,choices=USER_CHOICES,default=USER_USER)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone','email',]


    objects = MyAccountManager()

    def __str__(self):
        return self.username

    def has_perm(self,perm,obj=None):
        return self.is_admin
        
    def has_module_perms(self,app_label):
        return True
        
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)      


# # class QualityChecker