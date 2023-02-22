from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class shopregmodels(models.Model):

    shopname=models.CharField(max_length=30)
    address=models.CharField(max_length=30)
    shopid=models.IntegerField()
    email=models.EmailField()
    phone=models.IntegerField()
    pass1=models.CharField(max_length=20)
    pass2=models.CharField(max_length=20)
    def __str__(self):
        return self.shopname,self.address,self.shopid,self.email,self.phone


class productmodels(models.Model):
    shopid=models.IntegerField()
    productname = models.CharField(max_length=30)
    price = models.IntegerField()
    discription = models.CharField(max_length=100)
    image = models.FileField(upload_to='sample_app/static')
    def __str__(self):
        return self.productname

class profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    auth_token=models.CharField(max_length=100)
    is_verified=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)



#we have a user models
#user models                                          profile
#username , email , fn ,ln , password                 user auth is_  created

class cart(models.Model):
    userid=models.IntegerField()
    productname = models.CharField(max_length=30)
    price = models.IntegerField()
    discription = models.CharField(max_length=100)
    image = models.FileField()
    def __str__(self):
        return self.productname

class wishlist(models.Model):
    userid=models.IntegerField()
    productname = models.CharField(max_length=30)
    price = models.IntegerField()
    discription = models.CharField(max_length=100)
    image = models.FileField()
    def __str__(self):
        return self.productname

class buy(models.Model):
    productname = models.CharField(max_length=30)
    price = models.IntegerField()
    discription = models.CharField(max_length=100)
    image = models.FileField()
    quantity=models.IntegerField()

class customercardM(models.Model):
    cardname = models.CharField(max_length=30)
    cardnumber = models.IntegerField()
    carddate = models.CharField(max_length=30)
    scode = models.IntegerField()


class shopNotification(models.Model):
    content=models.CharField(max_length=200)
    date=models.DateField(auto_now_add=True)
    def __str__(self):
        return self.content

class userNotification(models.Model):
    content=models.CharField(max_length=200)
    date=models.DateField(auto_now_add=True)
    def __str__(self):
        return self.content








