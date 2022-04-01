from rest_framework import serializers
from private_messages.models import MessageBody





class MessageBodySerializer(serializers.ModelSerializer):
    #sender_name = serializers.SerializerMethodField()
    receiver_name = serializers.SerializerMethodField()

    
    class Meta:
        model = MessageBody
        fields = ["receiver_name", "sender", "receiver", "message", "is_read"]


    def get_receiver_name(self, obj):
        name = obj.username
        print(obj)
        return name