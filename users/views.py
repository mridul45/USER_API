from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

# from users.serializers import UserRegistrationSerializer
# from .serializers import *
from django.contrib.auth import authenticate
# from .renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .serializers import UserRegistrationSerializer,UserLoginSerializer,ProfileSerializer
from .models import *


def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }


class UserRegistrationView(APIView):
#   renderer_classes = [UserRenderer]
	def post(self, request, format=None):

		serializer = UserRegistrationSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.save()
		token = get_tokens_for_user(user)
		return Response({'token':token, 'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)
	


class UserLoginView(APIView):
#   renderer_classes = [UserRenderer]
	def post(self, request, format=None):

		serializer = UserLoginSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		email = serializer.data.get('email')
		password = serializer.data.get('password')
		user = authenticate(email=email, password=password)

		if user is not None:

			token = get_tokens_for_user(user)
			return Response({'token':token, 'msg':'Login Success',"email":email}, status=status.HTTP_200_OK)

		else:
			return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)
		


class ProfileView(APIView):
	# permission_classes = [IsAuthenticated]
	def post(self,request):
		serializer = ProfileSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data,status=status.HTTP_201_CREATED)
		return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
	


class ProfileDetailView(APIView):
	# permission_classes = [IsAuthenticated]
	def get_object(self,id):
		try:
			return Profile.objects.get(id=id)
		except Profile.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
	def get(self,request,id):

		profile = self.get_object(id)
		serializer = ProfileSerializer(profile)
		return Response(serializer.data)


	def put(self,request,id):

		profile = self.get_object(id)
		serializer = ProfileSerializer(profile,data=request.data)

		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)

		return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
	
	def delete(self,request,id):

		profile = self.get_object(id)
		profile.delete()
		return HttpResponse(status=status.HTTP_204_NO_CONTENT)