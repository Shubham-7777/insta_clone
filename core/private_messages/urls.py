

from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static


from private_messages.models import MessageBody
from private_messages.views import Message_List

app_name = 'private-messages-app'

urlpatterns = [
    path("private-messages/", Message_List.as_view(), name="private-messages-url"),
        
    
    
    
]
