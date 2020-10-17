from django.db import models



class User(models.Model):
    contact=models.IntegerField(max_length=10)
    otp=models.IntegerField(max_length=6,null=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.all


