from rest_framework import serializers
from users.models import UserProfile, Follow



class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user")
    class Meta:
        model = UserProfile
        fields = ["username", "first_name", "last_name", "profile_image", "website", "gender", "code", "phone_no", "secondary_no", "permanent_address", "temporary_address", "date_joined"]
        
        
        
        
class FollowSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.user.username")
    #followers = UserProfileSerializer(many=True)
    #following = UserProfileSerializer(many=True)
    #following = serializers.SerializerMethodField()
    #follow_details = serializers.SerializerMethodField()
    follow_details = serializers.SerializerMethodField()
    
    
    class Meta:
        model = Follow
        fields = ["user", "follow_details"]
                #"followers", "following"



    def get_follow_details(self, data):
        print(data, "data")
        follow = {}
        print(data._meta)
        print(dir(data.following.values_list("user__username")), "dir(data)")        
        follow["following"] = data.following.values_list("user__username", flat=True)        
        follow["followers"] = data.followers.values_list("user__username", flat=True)        
        return follow


"""
    def get_following(self, obj):
        if 'request' in self.context:
            print(self.context["request"], "self.context")
            request = self.context['request']            
            if obj in request.user.following.all():
                return True
        return False
"""

    
class SearchSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username")
    
    class Meta:
        model = UserProfile
        fields = ["user"]
      
