from cookbookapi.models.CbUser import CbUser
from cookbookapi.models.Category import Category
from typing import Match
from django.db import models


class Recipe(models.Model):

    title = models.CharField(max_length=50)
    info = models.CharField( max_length=250)
    picture = models.ImageField(upload_to='recipe_image_url', height_field=None, max_length=None, width_field=None, null=True)
    ingredients = models.CharField(max_length=300)
    directions = models.CharField(max_length=950)
    notes = models.CharField(max_length=350)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(CbUser, on_delete=models.CASCADE)
