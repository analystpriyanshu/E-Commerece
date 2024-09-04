from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class Category(models.Model):
    category_image=models.ImageField(upload_to="gallery",default=0)
    Category_name=models.CharField(max_length=200,default=0)
    def __str__(self):
         return self.Category_name

class Product_type(models.Model):
    enter_type=models.CharField(max_length=200,default=0)
    def __str__(self):
        return self.enter_type

class Product(models.Model):
    D=(
    ('HOT DEALS','HOT DEALS'),
    ('New Arraivels','New Arraivels'),
    )

    category=models.ForeignKey(Category,on_delete=models.CASCADE,default=0) 
    Prod_type=models.ForeignKey(Product_type,on_delete=models.CASCADE,default=0)
    prod_deal=models.CharField(choices=D,max_length=100,default=0)
    prod_name=models.CharField(max_length=100,default=0)
    Prod_descriptiontwo=models.CharField(max_length=2000,blank=True)
    Prod_descriptionthree=models.CharField(max_length=2000,blank=True)
    Prod_descriptionfour=models.CharField(max_length=2000,blank=True)
    Prod_descriptionfive=models.CharField(max_length=2000,blank=True)
    Prod_descriptionsix=models.CharField(max_length=2000,blank=True)
    prod_mrp=models.FloatField(default=0)
    prod_price=models.FloatField(default=0)
    prod_img=models.ImageField(upload_to='productimages',default=0)
    prod_img2=models.ImageField(upload_to='productimages',default=0)
    prod_img3=models.ImageField(upload_to='productimages',default=0)
    add_on=models.DateTimeField(auto_now_add=True,null=True)
    prod_outofstock=models.BooleanField(default=False)
    def __str__(self):
        return self.prod_name
# customer model
class ExtendedUser(User):
      user=models.OneToOneField(User,parent_link=True,primary_key=True,on_delete=models.CASCADE)
      phone_no=models.CharField(max_length=12,default=0)  
      alt_no=models.CharField(max_length=12,default=0)
      address=models.CharField(max_length=500,default=0)
      profile_pic=models.ImageField(upload_to='userpics')
      def __str__(self):
            return self.user.username

class order(models.Model):
    customer=models.ForeignKey(ExtendedUser,on_delete=models.CASCADE) 
    product_order=models.ForeignKey(Product,on_delete=models.CASCADE) 
    cust_ki_id=models.IntegerField(default=0)
    cust_ka_name=models.CharField(max_length=100,default=0)
    cust_ka_username=models.CharField(max_length=100,default=0)
    cust_ka_phone=models.CharField(max_length=12,default=0) 
    cust_ka_alt_no=models.CharField(max_length=12,default=0) 
    cust_ki_email=models.CharField(max_length=100,default=0)
    cust_ka_address=models.CharField(max_length=500,default=0)
    Product_ki_id=models.IntegerField(default=0)
    product_ki_img=models.ImageField(upload_to='productimages',default=0)
    Product_ki_quantity=models.IntegerField(default=1)
    product_ki_price=models.FloatField(default=0)
    product_ka_name=models.CharField(max_length=100,default=0)
    status=models.BooleanField(default=False)
    add_on=models.DateTimeField(auto_now_add=True,null=True)
    def __str__(self):
            return self.cust_ka_name




