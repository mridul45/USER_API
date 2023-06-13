from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
from .manager import *

class User(AbstractBaseUser):
        
	email = models.EmailField(
	verbose_name='Email',
	max_length=255,
	unique=True,
	)
	name = models.CharField(max_length=200)
	# tc = models.BooleanField()
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = UserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['name']

	def __str__(self):
		return self.name

	def has_perm(self, perm, obj=None):
		"Does the user have a specific permission?"
		# Simplest possible answer: Yes, always
		return self.is_admin

	def has_module_perms(self, app_label):
		"Does the user have permissions to view the app `app_label`?" 
		# Simplest possible answer: Yes, always
		return True

	@property
	def is_staff(self):
		"Is the user a member of staff?"
		# Simplest possible answer: All admins are staff
		return self.is_admin
	


class Profile(models.Model):

	user = models.ForeignKey(User,on_delete=models.CASCADE)
	username = models.CharField(max_length=200,null=True,blank=True)
	preferred_email = models.EmailField(max_length=200,null=True,blank=True)
	bio = models.TextField(null=True,blank=True)
	profile_pic = models.CharField(max_length=255,null=True,blank=True)

	def __str__(self):
		return self.username