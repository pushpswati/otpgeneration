from django.db import models



class User(models.Model):
    firstname=models.CharField(max_length=255,blank=True,null=True)
    lastname=models.CharField(max_length=255,blank=True,null=True)
    address=models.CharField(max_length=255,blank=True,null=True)
    email=models.EmailField(max_length=255,blank=True,null=True)
    token=models.CharField(max_length=255,blank=True,null=True)
    contact=models.IntegerField(blank=True,null=True)
    otp=models.IntegerField(blank=True,null=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return 'User contact: %s' % (self.contact)

class Jobs(models.Model):
    PENDING = 'PENDING'
    COMPLETED = 'COMPLETED'
    DELIVERED='DELIVERED'
    PARTIAL_PAYMENT='PARTIAL_PAYMENT'


    Job_statusChoices = (
        (PENDING, 'PENDING'),
        (COMPLETED, 'COMPLETED'),
        (DELIVERED, 'DELIVERED'),
    )
    Payment_status=(
        (PENDING, 'PENDING'),
        (PARTIAL_PAYMENT,"PARTIAL_PAYMENT"),
        (COMPLETED, 'COMPLETED'),

    )
    
    user=models.ForeignKey(User, related_name='user_media', on_delete=models.CASCADE)
    file_name=models.FileField(upload_to='user_documents',blank=True,null=True)
    quotation=models.FileField(upload_to='quotation',blank=True,null=True)
    description=models.TextField(blank=True,null=True)
    job_name=models.CharField(max_length=255,blank=True,null=True)
    job_type=models.CharField(max_length=255,blank=True,null=True)
    paper_material=models.CharField(max_length=255,blank=True,null=True)
    size=models.CharField(max_length=255,blank=True,null=True)
    quantity=models.IntegerField(blank=True,null=True)
    price=models.FloatField(blank=True,null=True)
    job_status = models.CharField(
        max_length=25,
        choices=Job_statusChoices,
        default=PENDING,
    )
    payment_status = models.CharField(
        max_length=25,
        choices=Payment_status,
        default=PENDING,
    )
    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'file_name','description',
                           'job_name','created')
        ordering = ['created']

    def __str__(self):
        return '%s __ Job_name:- %s __ Quantity:-- %s Job_Status:-- %s __ Payment:-- %s' % (self.user,self.job_name,self.quantity,self.job_status,self.payment_status)
    
class SliderImage(models.Model):
    """
    Wishpoint documents model
    """
    image_name = models.CharField(max_length=222, blank=True, null=True)
    image=models.ImageField(upload_to='media/package',blank=True,null=True)
    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ( 'image_name','image','created')
        ordering = ['created']

    def __str__(self):
        return 'Image_name: %s Uploaded_date: %s' % (self.image_name,self.created)