from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.core import serializers

from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.status import (
	HTTP_400_BAD_REQUEST,
	HTTP_404_NOT_FOUND,
	HTTP_200_OK
)
from rest_framework.views import APIView

from . import models

class HomePageAPIView(APIView):
	"""API View for the home page
	"""
	permission_classes = [permissions.AllowAny]

	def get(self, request, *args, **kwargs):
		return Response(status=HTTP_200_OK)