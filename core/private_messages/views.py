from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.
from users.models import UserProfile
from private_messages.models import MessageBody
from private_messages.serializers import MessageBodySerializer




class Message_List(APIView):
    
    
    def get(self, request, sender, receiver):
        messages = MessageBody.objects.filter(sender__id=sender, receiver__id=receiver, is_read=False)
        serializer = MessageBodySerializer(many=True, context = {"request", request})
        for message in messages:
            message.is_read=True
            message.save()
            return Response({"data" : serializer.data})
        

    def post(self, request):
        get_receiver = UserProfile.objects.filter(user__username=request.data["receiver"]).first()
        login_uuid = UserProfile.objects.filter(user__username=request.user).values_list("code", flat=True)[0]
        request.data["sender"] = login_uuid
        receiver_uuid = UserProfile.objects.filter(user__username=request.data["receiver"]).values_list("code", flat=True)[0]
        
        request.data["receiver"] = receiver_uuid 
        print(get_receiver) 
        print(request.data)
        message_serializer = MessageBodySerializer(data=request.data)
        if message_serializer.is_valid(raise_exception=True):
            message_serializer.save()
            return Response({"data": message_serializer.data})
        else:
            return Response({"ERRORS": message_serializer.errors})
            