from django.db import models
from django.contrib.auth.models import User
from django import forms




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    ime = models.CharField(max_length=500, default="")
    prezime = models.CharField(max_length=500, default="")
    adresa = models.CharField(max_length=250, default="")
    grad = models.CharField(max_length=200, default="")
    broj_telefona = models.CharField(max_length=12, default="")

    def __str__(self):
        return f'{self.user.username} Profile'


class Product(models.Model):
    ime = models.CharField(max_length=500, null=True)
    kategorija=models.CharField(max_length=50, null=True)
    cijena = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.ime

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''

        return url


class Order(models.Model):
    customer = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping


    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems ])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.cijena * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    adresa = models.CharField(max_length=500, null=True)
    grad = models.CharField(max_length=500, null=True)
    postanskibroj = models.CharField(max_length=500, null=True)
    drzava = models.CharField(max_length=500, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.adresa

