from django.db import models

# Create your models here.
class Todo(models.Model):
    Num1 = models.FloatField()
    town = models.CharField(max_length = 100)
    Num2 = models.CharField(max_length = 100)
    Geography = models.CharField(max_length = 100)
    longitude = models.FloatField()
    latitude = models.FloatField()
    irrigation = models.CharField(max_length = 100)
    groundwater= models.FloatField()
    drawdown = models.FloatField()
    final = models.FloatField()
    age = models.FloatField()
    welldeep = models.FloatField()
    wellr = models.FloatField()
    mertial = models.CharField(max_length = 100)
    elevation = models.FloatField()
    power = models.FloatField()
    lift = models.FloatField()
    flow = models.FloatField()
    convert = models.FloatField()

    def __str__(self):
        return f"Num1: {self.Num1}, Town: {self.town}"
