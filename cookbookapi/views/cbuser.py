from django.contrib.auth.models import User
from django.http.response import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from cookbookapi.models.CbUser import CbUser




class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for users"""

    class Meta:
        model= User
        fields = ('id', 'username', 'first_name', 'last_name', 'date_joined' ) 

class CbUserSerailizer(serializers.ModelSerializer):
    """JSON cbuser serializer"""
    user = UserSerializer()
    class Meta:
        model = CbUser
        fields = ('id','bio','user')


class CbUsers(ViewSet):

    def retrieve(self,request,pk=None):
        try:
            cbuser = CbUser.objects.get(pk = pk)
            serializer = CbUserSerailizer(cbuser, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
