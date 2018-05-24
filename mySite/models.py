from django.db import models

# Create your models here.
from django.db import models

# Create your models here.


class User(models.Model):

    gender = (
        ('male', "男"),
        ('female', "女"),
    )

    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default="男")
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "用户"
        verbose_name_plural = "用户"


class ShopInfo(models.Model):
    goods_name = models.CharField(max_length=255)
    goods_price = models.CharField(max_length=255)
    goods_shop = models.CharField(max_length=255)
    goods_comments = models.CharField(max_length=255)
    goods_url = models.CharField(max_length=250)
    goods_searcher = models.CharField(max_length=255)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.goods_name

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "商品信息"
        verbose_name_plural = "商品信息"


class SearchRecord(models.Model):
    searcher = models.CharField(max_length=255)
    keyword = models.CharField(max_length=255)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.searcher

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "搜索记录"
        verbose_name_plural = "搜索记录"