from django.shortcuts import render
from rest_framework import views,parsers,status
from rest_framework.response import Response
from . import serializers
# Create your views here.

class TestView(views.APIView):
    parser_classes = [parsers.FormParser,parsers.MultiPartParser]
    serializer_class = serializers.TestSerializer
    def post(self,request):
        serializer = self.serializer_class(request.user, data = request.data)
        if serializer.is_Valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED )
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)