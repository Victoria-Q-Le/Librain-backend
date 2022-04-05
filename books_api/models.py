from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Book(models.Model):
    user = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    name = models.CharField(max_length = 200, null = True, blank = True)
    author = models.CharField(max_length = 200, null = True, blank = True)
    image = models.ImageField(null = True, blank = True)
    description = models.TextField(null = True, blank = True)
    rating = models.DecimalField(max_digits = 7, decimal_places = 2, null = True, blank = True)
    numReviews = models.IntegerField (null = True, blank = True, default = 0)
    price = models.DecimalField(max_digits = 7, decimal_places = 2, null = True, blank = True)
    store = ArrayField(models.CharField (max_length = 200, null = True, blank = True))
    countInStock = models.IntegerField (null = True, blank = True, default = 0)
    createdAt = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.name

#A User can create/have many products so the realtionship betwenn User and Book is one to many
#on_delete was set to NULL because I dont want the Book gets deleted if whoever entered that Book into the database gets fired
#null = False, means that I allow this field to be empty in the database.
#blank = True, we can fill out the form and arent required to fill out this field

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete = models.SET_NULL, null = True)
    user = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    name = models.CharField(max_length = 200, null = True, blank = True)
    rating = models.IntegerField (null = True, blank = True, default = 1)
    comment = models.TextField(null = True, blank = True)

    def __str__(self):
        return str(self.book)

#A User can leave a comment for multiple books and one book can have multiple comments from different users

class Order(models.Model):
    user = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    paymentMethod = models.CharField(max_length = 200, null = True, blank = True)
    tax = models.DecimalField(max_digits = 7, decimal_places = 2, null = True, blank = True)
    shipping = models.DecimalField(max_digits = 7, decimal_places = 2, null = True, blank = True)
    total = models.DecimalField(max_digits = 7, decimal_places = 2, null = True, blank = True)
    isPaid = models.BooleanField(default = False)
    paidAt = models.DateTimeField(auto_now_add = False, null = True, blank = True)
    isDelivered = models.BooleanField(default = False)
    deliveredAt = models.DateTimeField(auto_now_add = False, null = True, blank = True)
    createdAt = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return str(self.createdAt)

class OrderItem(models.Model):
    book = models.ForeignKey(Book, on_delete = models.SET_NULL, null = True)
    order = models.ForeignKey(Order, on_delete = models.SET_NULL, null = True)
    name  = models.CharField(max_length = 200, null = True, blank = True)
    qty = models.IntegerField (null = True, blank = True, default = 0)
    price = models.DecimalField(max_digits = 7, decimal_places = 2, null = True, blank = True)
    image = models.CharField(max_length = 200, null = True, blank = True)

    def __str__(self):
        return str(self.order)


class ShippingAddress(models.Model):
    order = models.OneToOneField(Order, on_delete = models.CASCADE , null = True, blank = True)
    address = models.CharField(max_length = 200, null = True, blank = True)
    city = models.CharField(max_length = 200, null = True, blank = True)
    zip = models.CharField(max_length = 5, null = True, blank = True)
    state = models.CharField(max_length = 2, null = True, blank = True)
    shipping = models.DecimalField(max_digits = 7, decimal_places = 2, null = True, blank = True)

    def __str__(self):
        return str(self.address)
#The Order is only has one shipping address
#on_delete = models.CASCADE means that when someone delete the Order, the sipping address will also begone
