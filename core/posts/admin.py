from django.contrib import admin
from .models import Posts, Comments, Votes, Tags
# Register your models here.

admin.site.register(Posts)
admin.site.register(Comments)
admin.site.register(Votes)
admin.site.register(Tags)
