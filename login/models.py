from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Profile(models.Model):
    CATEGORIES = (
        ('STUD','Student'),
        ('DRIV','Driver'),
    )
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100,blank=True)
    last_name = models.CharField(max_length=100,blank=True)
    email = models.CharField(max_length=150)
    category = models.CharField(max_length=4,choices=CATEGORIES,default='STUD')
    phone = models.CharField(max_length=10)
    signup_confirmation = models.BooleanField(default= False)
    def __str__(self):
        return self.user.username

@receiver(post_save,sender=User)
def update_profile(sender,instance,created, **kwargws):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class Journey(models.Model):
    PLACES = (
        ('VAL','Vallikavu'),
        ('KYJ','Kayamkulam'),
        ('KPI','Karunagapalli')
    )
    profilename = models.ForeignKey(User,on_delete = models.CASCADE)
    source= models.CharField(max_length=3,choices=PLACES)
    destination= models.CharField(max_length=3,choices=PLACES)
    datefield = models.DateField()
    timefield = models.TimeField()
    preference= models.IntegerField()
    status = models.CharField(max_length=100)

class Teams(models.Model):
    jid=models.ForeignKey(Journey,on_delete=models.CASCADE)
    pid=models.ForeignKey(Profile,on_delete=models.CASCADE)
    arri = models.CharField(max_length=10,default='None')
    teamid=models.IntegerField(default=0)
