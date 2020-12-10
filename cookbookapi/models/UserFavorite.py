from cookbookapi.models.CbUser import CbUser
from cookbookapi.models.Recipe import Recipe
from django.db import models

class UserFavorite (models.Model):

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    cbuser = models.ForeignKey(CbUser, on_delete=models.CASCADE)