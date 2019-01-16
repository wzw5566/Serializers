# -*- coding: UTF-8 -*-
from django.http import HttpResponse,JsonResponse
from rest_framework_jwt.utils import jwt_decode_handler
from django.contrib.auth import get_user_model
from users.serializers import UserDetailSerializer

def get_user_info(request):

    User = get_user_model()
    if request.method=='GET':
        token_str=request.GET.get('token')
        token = token_str.split()[1]
        toke_user = []
        toke_user = jwt_decode_handler(token)
        user_id = toke_user["user_id"]
        user_info = User.objects.get(pk=user_id)
        serializer = UserDetailSerializer(user_info)
        data = {

            "data": serializer.data,
            "code": 20000
        }

        return JsonResponse(data)
