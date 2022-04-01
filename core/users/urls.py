

from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from users.views import Recent5Users, CurrentUser, FollowUser, UnFollowUser, UserFollowDetails, SearchUser, LoginAPI
#from django.contrib.auth.views import login, logout
from users.views import test_template


app_name = 'users-app'

urlpatterns = [

    path("test/", test_template, name="test_url"),
    
    
    path("recent-users/", Recent5Users.as_view(), name="recent_users_url"),

    #path("current-user/", CurrentUser.as_view(), name="current-user-url"),
    path("", CurrentUser.as_view(), name="home"),

    path("follow-user/", FollowUser.as_view(), name="follow-user-url"),

    path("un-follow-user/", UnFollowUser.as_view(),name="un-follow-user-url"),

    path("following-list/", UserFollowDetails.as_view(),name="following-list-url"),

    path("search/<str:user>/", SearchUser.as_view(),name="search-user-url"),

    #path('login/', 'django.contrib.auth.views.login',name="my_login")

    path("login/", LoginAPI.as_view(), name="login-url"),
    


]