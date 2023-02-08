from django.db import models
from datetime import date, timedelta
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    position = models.CharField(max_length=50)
    image = models.ImageField(upload_to='profile', blank = True, default = '')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.username

class Debtor(models.Model):
    user = models.ForeignKey("api.User", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    maiden = models.CharField(max_length=50, null = True, blank = True)
    surname = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    phonenumber = models.CharField(max_length=10)
    id_number = models.CharField(max_length=14)

    
    status = models.CharField(max_length=50, default = '', blank = True )
    created = models.DateField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.name} {self.surname}"

class Product(models.Model):
    debtor = models.ForeignKey("api.Debtor", on_delete=models.CASCADE)
    product = models.CharField(max_length=50)
    product_serial_no = models.CharField(max_length=50)
    product_selling_price = models.DecimalField(max_digits=6, decimal_places=2, null = True, blank = True, default= 0)
    product_details = models.CharField(max_length= 100)

    def __str__(self) -> str:
        return f'{self.product}'
class Payment(models.Model):
    product = models.OneToOneField("api.Product", on_delete=models.CASCADE, primary_key=True)
    deposit = models.DecimalField(max_digits=6, decimal_places=2, null = True, blank = True, default= 0)
    first_payment = models.DecimalField(max_digits=6, decimal_places=2,  default= 0, null = True, blank = True)
    second_payment = models.DecimalField(max_digits=6, decimal_places=2,   default= 0, null = True, blank = True)
    final_payment = models.DecimalField(max_digits=6, decimal_places=2, default= 0, null = True, blank = True)
    is_fully_paid = models.CharField(max_length=50, default = 'no', null=True, blank = True)

    # setting due dates
    first_payment_due_date = models.DateField(default = date.today() + timedelta(days=30), null = True)
    second_payment_due_date = models.DateField(default = date.today() + timedelta(days=60), null = True)
    final_payment_due_date = models.DateField(default = date.today() + timedelta(days=90), null = True)

    # def __str__(self) -> str:
    #     return self.debtor


class Work(models.Model):
    debtor = models.OneToOneField("api.Debtor", related_name='work',  on_delete=models.CASCADE, primary_key=True)
    employer = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    employer_contact = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.employer