from django.db import models
from account import models 
from myadmin.models import *


# Create your models here.
CHOICES = (
    ('bear', 'BEAR'),
    ('bull', 'BULL'),
     ('single', 'SINGLE'),
    ('twin', 'TWIN'),
)

RESULTS = (
    ('pending', 'PENDING'),
    ('success', 'SUCCESS'),
     ('failed', 'FAILED'),
)


class CoinModel(models.Model):
    customer = models.ForeignKey('account.User',on_delete=models.CASCADE,default=None)
    coin_type = models.ForeignKey(CoinTypeModel,on_delete=models.CASCADE,default=None)
    network_type = models.ForeignKey(NetworkModel,on_delete=models.CASCADE,default=None)
    quantity = models.IntegerField(default=0)
    time = models.DateTimeField(default=datetime.now)

class DepositModel(models.Model):
    customer = models.ForeignKey('account.User',on_delete=models.CASCADE,default=None)
    coin_type = models.ForeignKey(CoinTypeModel,on_delete=models.CASCADE,default=None)
    network_type = models.ForeignKey(NetworkModel,on_delete=models.CASCADE,default=None)
    quantity = models.BigIntegerField(default=0)
    screenshot = models.ImageField(default=None,null=True,blank=True)
    status = models.BooleanField(default = False)
    time = models.DateTimeField(default=datetime.now)

class WithdrawModel(models.Model):
    customer = models.ForeignKey('account.User',on_delete=models.CASCADE,default=None)
    coin_type = models.ForeignKey(CoinTypeModel,on_delete=models.CASCADE,default=None)
    network_type = models.ForeignKey(NetworkModel,on_delete=models.CASCADE,default=None)
    quantity = models.BigIntegerField(default=0)
    user_link_address = models.TextField(default=None)
    status = models.BooleanField(default = False)
    time = models.DateTimeField(default=datetime.now)

class DepositHistoryModel(models.Model):
    deposit = models.ForeignKey(DepositModel,on_delete=models.CASCADE,default=None)
    time = models.DateTimeField(default=datetime.now)

class WithdrawHistoryModel(models.Model):
    withdraw = models.ForeignKey(WithdrawModel,on_delete=models.CASCADE,default=None)
    time = models.DateTimeField(default=datetime.now)

class RandomModel(models.Model):
    a = models.CharField(max_length=20)
    b = models.CharField(max_length=20)
    c = models.CharField(max_length=20)
    room = models.IntegerField(default=None,null=True,blank=True)
    status = models.CharField(default=None,null=True,blank=True,max_length=20)
    roundno = models.IntegerField(default=None,null=True,blank=True)
    total = models.IntegerField(default=None,null=True,blank=True)

class UserChoiceModel(models.Model):
    choice = models.CharField(choices=CHOICES,max_length=20,default='bear')
    amount = models.IntegerField()
    room = models.IntegerField(default=None)
    roundno = models.IntegerField()
    user = models.ForeignKey('account.User',on_delete=models.CASCADE,default=None)
    result = models.CharField(choices=RESULTS,max_length=20,default='pending')