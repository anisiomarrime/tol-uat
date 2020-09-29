from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now


class UserTokens(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    token = models.CharField(max_length=150)
    objects = models.Manager()


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)
    objects = models.Manager()


class City(models.Model):
    name = models.CharField(max_length=150, unique=True)
    objects = models.Manager()


class Package(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    max_posts = models.IntegerField()
    post_duration = models.IntegerField()
    is_premium = models.BooleanField()
    objects = models.Manager()


class Seller(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    cash = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    photo = models.CharField(max_length=250, default='admin.jpg')
    package = models.ForeignKey(Package, on_delete=models.CASCADE, default=1)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    address = models.CharField(max_length=150, default='Moçambique')
    mobile = models.CharField(max_length=9)
    mobile_alternative = models.CharField(max_length=9, default='')
    status = models.IntegerField(default=1)
    is_verified = models.BooleanField(default=False)
    total_posts = models.IntegerField(default=0)
    objects = models.Manager()


class Doc(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, editable=False)
    photo = models.CharField(max_length=255, default='avatar.jpg')
    approved = models.BooleanField(default=False)
    objects = models.Manager()


class Post(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    thumb = models.CharField(max_length=255, default='avatar.jpg')
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    status = models.IntegerField(default=0)
    description = models.TextField(default='Ola! estou no So Boladas...')
    views = models.IntegerField(default=0)
    exp = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=now)
    objects = models.Manager()


class Payment(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE, default=1)
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    reference = models.CharField(max_length=50)
    comment = models.TextField(default='Ola! quero fazer o upgrade.')
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)
    objects = models.Manager()


class UpdateRequest(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=now)
    objects = models.Manager()


class Photo(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    photo = models.CharField(max_length=255, default='avatar.jpg')
    objects = models.Manager()