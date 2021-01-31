from rest_framework import serializers
from .models import Posts
class PostsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Posts
        fields = ['id','title','body']

class TotalPostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Posts
        fields = ['userID','id','title','body']