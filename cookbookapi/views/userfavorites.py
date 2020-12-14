from django.core.exceptions import ValidationError
from django.db.models import fields
from cookbookapi.views.recipe import RecipeSerializer
from cookbookapi.models.Recipe import Recipe
from cookbookapi.models.UserFavorite import UserFavorite
from rest_framework.response import Response
from rest_framework import serializers,status
from rest_framework.viewsets import ViewSet
from cookbookapi.models.CbUser import CbUser





class CbuserSerializer(serializers.ModelSerializer):
    """JSON serializer for user"""
    class Meta:
        model = CbUser
        fields = ('id','user')
        


class RecipeSerializer(serializers.ModelSerializer):
    """JSON serializer for recipe"""
    class Meta:
        model = Recipe
        fields = ('id','title')
       


class UserFavoriteSerializer(serializers.ModelSerializer):
    """JSON serializer for user favorites"""

    cbuser = CbuserSerializer(many=False)
    recipe = RecipeSerializer(many=False)
    class Meta:
        model = UserFavorite
        fields = ('id','cbuser','recipe')
        depth = 1



class UserFavorites(ViewSet):

 

    def create(self, request):
        """Handle POST operatoins when a user favorites a new recipe"""

        #create a new instance of a userfavorite using the model
        # find the user associated with the request and find the recipe they favorited
        # and set properties, then save
        user_favorite = UserFavorite()
        cbuser = CbUser.objects.get(user = request.auth.user)
        recipe = Recipe.objects.get(pk = request.data['recipe_id'])

        user_favorite.recipe = recipe
        user_favorite.cbuser = cbuser

        try:
            user_favorite.save()
            serializer = UserFavoriteSerializer(user_favorite, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


    def list(self, request):
        """Handle GET request to user favorites resource"""

        user_favorites = UserFavorite.objects.all()

        serializer = UserFavoriteSerializer(user_favorites,many=True, context={'request': request})
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single favorite"""

        try:
            user_favorite = UserFavorite.objects.get(pk=pk)
            user_favorite.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except UserFavorite.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
