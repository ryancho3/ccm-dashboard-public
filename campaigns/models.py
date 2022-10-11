from django.db import models
from django.contrib.auth.models import User


class School(models.Model):
    code = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    

class Campaign(models.Model):
    code = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=250)
    link_ios = models.URLField(max_length=200, blank=True, null=True)
    link_android = models.URLField(max_length=200, blank=True, null=True)
    schools = models.ManyToManyField(School)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name


class Impression(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Impression: " + self.campaign.code + "/" + self.school.code + "/" + str(self.datetime)

class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.ManyToManyField(School)

    def __str__(self):
        return self.user.first_name

# Create your models here.
