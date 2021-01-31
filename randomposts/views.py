from django.shortcuts import render
from .serializers import PostsSerializer,TotalPostSerializer
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from .models import Posts
from rest_framework import permissions,status,generics
from .permissions import IsOwner
# Create your views here.

class PostsListAPIView(ListCreateAPIView):
    serializer_class = PostsSerializer
    queryset = Posts.objects.all()
    permission_classes= (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save(userID=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(userID=self.request.user)

class PostsDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = PostsSerializer
    queryset= Posts.objects.all()
    permission_classes= (permissions.IsAuthenticated,IsOwner,)
    lookup_field = "id"

    def perform_create(self, serializer):
        return serializer.save(userID=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(userID=self.request.user)

class TotalPostAPIView(generics.GenericAPIView):
    serializer_class = TotalPostSerializer
    permission_classes= (permissions.IsAuthenticated,)

    def get(self, request):
        queryset = Posts.objects.all()
        serializer = self.serializer_class(queryset,many=True)
        
        return Response(serializer.data,status=status.HTTP_200_OK)
