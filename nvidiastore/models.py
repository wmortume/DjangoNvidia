from django.db import models


class Customer(models.Model):
    username = models.CharField(max_length=20, null=False)

    def __str__(self):
        return self.username


class Tag(models.Model):
    name = models.CharField(max_length=20, null=False)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=20, null=False)
    price = models.FloatField(null=False)
    image_url = models.CharField(max_length=500, null=False)
    url = models.CharField(max_length=20, null=False)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField(null=False)
