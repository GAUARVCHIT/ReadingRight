from django.db import models
from authentication.models import User
# Create your models here.

class Posts(models.Model):

    userID=models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(null=True,blank=False,max_length=255)
    body = models.TextField(null=True,blank=False)