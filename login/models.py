from django.db import models

# Create yofrom django.db import models

class RegisterUser(models.Model):
    username=models.CharField(max_length=100,blank=False)
    password=models.CharField(max_length=100,blank=False)
    email=models.CharField(max_length=100,blank=False)


    def __str__(self):
        return self.username
