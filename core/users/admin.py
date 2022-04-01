from django.contrib import admin
from users.models import UserProfile, Follow
#Contacc_Info
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Follow)
#admin.site.register(Contact_Info)