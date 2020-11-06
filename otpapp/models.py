from django.db import models



class User(models.Model):
    firstname=models.CharField(max_length=255,blank=True,null=True)
    lastname=models.CharField(max_length=255,blank=True,null=True)
    address=models.CharField(max_length=255,blank=True,null=True)
    email=models.EmailField(max_length=255,blank=True,null=True)
    token=models.CharField(max_length=255,blank=True,null=True)
    contact=models.IntegerField(max_length=10)
    otp=models.IntegerField(max_length=6,null=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)


    # def __str__(self):
    #     return self.all

class Media(models.Model):
    file_name=models.FileField(upload_to='user_documents',blank=True,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.file_name