from django.db import models


class Branch(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField()
    desc = models.CharField(max_length=200)
    desc2 = models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField()
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE,related_name='Doctor')
    desc = models.CharField(max_length=200)
    desc2 = models.CharField(max_length=100,blank=True, null=True)
    
    def __str__(self):
        return self.name
    
class Patient(models.Model):
    name = models.CharField(max_length=100)
    adress = models.CharField(max_length=100, blank=True, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='Doctor')
    book = models.DateTimeField()
    desc = models.CharField(max_length=110)
    
    def __str__(self):
        return self.name
    
    
    
    
