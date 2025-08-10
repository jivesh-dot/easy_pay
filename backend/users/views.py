from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status

from core.generic_responses import success_response, error_response
from users.models import User
import users.serializers as user_serializer

import logging
import traceback


class RegisterView(APIView):
    """
    POST /api/auth/register
    Body: [email, password, business_name]
    """
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = user_serializer.RegisterSerializer(data=request.data)
            if not serializer.is_valid():
                return error_response(serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)
            
            if User.objects.filter(username=request.data.get('email')).exists():
                return error_response({"detail": "email already exists"}, status_code=status.HTTP_400_BAD_REQUEST)

            serializer.save()

            return success_response(serializer.data, status_code=status.HTTP_201_CREATED)

        except IntegrityError as e:
            return error_response({"detail": "User with given credentials already exists"},
                                  status_code=status.HTTP_400_BAD_REQUEST)
        except Exception:
            logging.error(f'#users#views#RegisterView#post#exception={traceback.format_exc()}')
            return error_response('Server Error', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, generic=True)
