import base64
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from cookbookapi.models.Category import Category
from cookbookapi.models.CbUser import CbUser
from cookbookapi.models.Recipe import Recipe
from django.core.files.base import ContentFile
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers,status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.http.response import HttpResponseServerError
from rest_framework.filters import SearchFilter



class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for users"""

    class Meta:
        model= User
        fields = ('id', 'username' ) 

class AuthorSerializer(serializers.ModelSerializer):
    """JSON serializer for Author"""

    user = UserSerializer(many=False)

    class Meta:
        model = CbUser
        fields = ('user' ,)

class RecipeSerializer(serializers.ModelSerializer):
    """JSON serializer for Recipes"""

    author = AuthorSerializer(many=False)

    class Meta:
        model = Recipe
        fields = ('id', 'title', 'info', 'ingredients','directions',
                'notes', 'category', 'author', 'picture')
        depth = 2




class Recipes(ViewSet):

    permission_classes = (IsAuthenticatedOrReadOnly,)


    def create(self,request):


        new_recipe = Recipe()
        new_recipe.title = request.data['title']
        new_recipe.info = request.data['info']
        new_recipe.ingredients = request.data['ingredients']
        new_recipe.directions = request.data['directions']
        new_recipe.notes = request.data['notes']
        new_recipe.category = Category.objects.get(pk=request.data['category'])

        cbuser = CbUser.objects.get(user = request.auth.user)
        new_recipe.author = cbuser

        if "picture" in request.data:
            format, imgstr = request.data["picture"].split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f'{new_recipe.id}-{request.data["title"]}.{ext}')

            new_recipe.picture = data


        new_recipe.save()

        serializer = RecipeSerializer(
            new_recipe, context={'request': request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)



    def destroy(self, request, pk=None):

        try:
            recipe = Recipe.objects.get(pk=pk)
            recipe.delete()

            return Response({}, status= status.HTTP_204_NO_CONTENT)


        except Recipe.DoesNotExist as ex:
            return Response({}, status = status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        
        cbuser = CbUser.objects.get(user = request.auth.user)

        recipe = Recipe.objects.get(pk=pk)
        recipe.title = request.data['title']
        recipe.info = request.data['info']
        recipe.ingredients = request.data['ingredients']
        recipe.directions = request.data['directions']
        recipe.notes = request.data['notes']

        recipe.category = Category.objects.get(pk=request.data['category'])

        recipe.author = cbuser

        if "picture" in request.data:
            format, imgstr = request.data["picture"].split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f'{recipe.id}-{request.data["title"]}.{ext}')

            recipe.picture = data

        recipe.save()

        return Response({}, status= status.HTTP_204_NO_CONTENT)

    

    def list(self, request):

        recipes = Recipe.objects.all()

        user = self.request.query_params.get('user', None)
        search = self.request.query_params.get('search', None)

        if user is not None:
            recipes = recipes.filter(author = user)
        if search is not None:
            recipes = recipes.filter(Q(title__icontains=search) | Q(ingredients__icontains=search))
        

        serializer = RecipeSerializer(recipes, many=True, context={'request': request})
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        try:
            recipe = Recipe.objects.get(pk=pk)
            serializer = RecipeSerializer(recipe, context={'request': request})
            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

    

