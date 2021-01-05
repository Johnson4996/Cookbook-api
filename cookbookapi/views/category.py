from cookbookapi.models.Category import Category
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers,status
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for categories"""

    class Meta:
        model = Category
        fields = ('id', 'label')


class Categories (ViewSet):

    def list(self,request):

        categories = Category.objects.all()

        #can add params here example: category = self.request.query_params.get('category', None)
        #then adding if category is not None:
            #products = products.filter(category__id=category) for each param supported

        serializer = CategorySerializer(categories, many=True, context={'request': request})
        return Response(serializer.data)