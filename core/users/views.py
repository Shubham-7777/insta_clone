#from termios import CKILL
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.serializers import UserProfileSerializer, FollowSerializer, SearchSerializer
from users.models import UserProfile, Follow
from django.db.models import Q
from posts.views import get_logged_in_user
#from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import renderers
# Create your views here.


class LoginAPI(APIView):
    
    def get(self, request):
        return render(request, template_name="registration/login.html")
    
    
    def post(self, request):
        print("EXECUTING CORRECTLy")
        print(request.data["username"])
        print(request.data["password"])
        
        pass






class Recent5Users(APIView):
    
    
    
    def get(self, request):
        last_five = UserProfile.objects.all().order_by('-date_joined')[:5]
        serializer = UserProfileSerializer(last_five, many=True, context={"request": request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    
    
class UserFollowDetails(APIView):
    
    
    
    def get(self, request):
        user = request.user
        data = UserProfile.objects.filter(user__username=user).first()
        print(data)
        #follow_details = Follow.objects.filter(user__user=user)
        #follow_s = FollowSerializer(follow_details, many=True, context = {"request" : request})
        followers = Follow.objects.filter(user__user=user).values_list("followers__user__username", flat=True)
        following = Follow.objects.filter(user__user=user).values_list("following__user__username", flat=True)        
        serializer_data = UserProfileSerializer(data, context = {"request" : request})
        new_serializer = serializer_data.data
        new_serializer["followers"] = followers
        new_serializer["following"] = following
        return Response({"new_serializer" :new_serializer}) #"user_data" : serializer_data.data, "follow_data" : follow_s.data 
        
        
        
class CurrentUser(APIView):
    renderer_classes = [renderers.TemplateHTMLRenderer]

    
    
    def get(self, request):
        
        current_user = request.user
        obj = UserProfile.objects.get(user=current_user)
        serializer = UserProfileSerializer(obj)
        data=serializer.data
        context = {"data" : data}
        return Response(context, status=status.HTTP_200_OK, template_name="users/user-profile.html")



    def put(self, request):
        current_user = request.user
        print(request.data, "request.data")
        found_user = UserProfile.objects.get(user__username=current_user)
        serializer_data = UserProfileSerializer(found_user, data = request.data, partial=True)
        if serializer_data.is_valid(raise_exception=True):
            serializer_data.save()
            return Response(serializer_data.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)
        
        


class FollowUser(APIView):
    

    
    def put(self, request):
        logged_in_user = Follow.objects.filter(user=get_logged_in_user(request)).first()
        to_follow = UserProfile.objects.filter(user__username=request.data["follow"]).first()
        logged_in_user.following.add(to_follow)
        logged_in_user.save()
        logged_in_user_for_followers = UserProfile.objects.get(user__username=request.user)
        add_follower = Follow.objects.filter(user__user__username=request.data["follow"]).first()
        add_follower.followers.add(logged_in_user_for_followers)
        add_follower.save()
        obj = Follow.objects.get(user__user__username=request.user)
        serializer_data = FollowSerializer(obj, data=request.data, partial=True, context= {"request" :  request})
        if serializer_data.is_valid(raise_exception=True ):
            serializer_data.save()
            return Response(serializer_data.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)
            
            
                
                
class UnFollowUser(APIView):
            
                

    def put(self, request):
        user_to_unfollow = request.data["unfollow"]
        logged_in_user = Follow.objects.get(user__user__username=request.user)
        to_unfollow = UserProfile.objects.get(user__username=user_to_unfollow)
        print(to_unfollow)
        logged_in_user.following.remove(to_unfollow)
        logged_in_user.save()
        logged_in_user_for_followers = UserProfile.objects.get(user__username=request.user)
        remove_follower = Follow.objects.get(user__user__username=user_to_unfollow)
        remove_follower.followers.remove(logged_in_user_for_followers)
        remove_follower.save()
        data = Follow.objects.get(user__user=request.user)
        serializer_data = FollowSerializer(logged_in_user, data=request.data, partial=True)
        if serializer_data.is_valid(raise_exception=True):
            serializer_data.save()
            return Response(serializer_data.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)




class SearchUser(APIView):
    
    
    
    def get(self, request, user):
        print(dir(self.request))
        obj = self.kwargs.get('user')
        search_user = UserProfile.objects.filter(
            (Q(user__username__icontains = obj)) |
            (Q(user__first_name__icontains = obj)) |
            (Q(user__last_name__icontains = obj))
        )
        
        data = SearchSerializer(search_user, many=True)
        return Response(data.data, status=status.HTTP_200_OK)
    
    
    
    
    
def test_template(request):
    a = "TESTING TEMPLATE"
    context = { "a" : a}
    template_name = "users/test.html"
    return render(request, template_name, context)
