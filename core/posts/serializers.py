from rest_framework import serializers
from posts.models import Posts, Comments, Votes, Tags
from users.models import UserProfile
from users.serializers import UserProfileSerializer


class TagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tags
        fields = ["tag"]




class PostsSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.user.username", read_only=True)
    #username = serializers.CharField(default=serializers.CurrentUserDefault())
    #hashtags = TagSerializer(many=True)
    hashtags = serializers.SerializerMethodField()
    
    
    
    class Meta:
        model = Posts
        fields = ["user", "username", "id", "image", "caption", "hashtags"]
    
    
    def get_hashtags(self, data):
        print(dir(data.hashtags))
        return data.hashtags.values_list("tag", flat=True)
    
    """
    def get_username(self, obj):
        #return obj.user.user.username
        #user = self.context.get("request").user
        #user =  self.context['request']
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            print(user, "user")
            return user
        """
        
        
class CommentsSerializer(serializers.ModelSerializer):
    #post = serializers.SerializerMethodField()
    username = serializers.CharField(source="user.user.username")
    
    class Meta:
        model = Comments
        fields = ["user", "username",  "id", "image", "message"]
                #"post",
    
    """
    def get_post(self, data):
        print(data.image.id, "data")
        print(dir(data))
        post = Posts.objects.filter(id=data.image.id)
        print(self.context, "self.context")
        return post
    """    
          

class VotesSerializer(serializers.ModelSerializer):
    #user = UserProfileSerializer()
    name = serializers.SerializerMethodField()
    #user = serializers.CharField(source="user.user.username")
    #image = PostsSerializer()
    #post = PostsSerializer()
    vote_id = serializers.SerializerMethodField()
    
     
    class Meta:
        model = Votes
        #depth = 1

        fields = [ "image_id", "vote_id", "name", "vote"]
                #name1

    def get_vote_id(self, data):
        return data.id


    def get_name(self, obj):
        print(obj.user.user.username)
        #user = UserProfile.objects.filter(user__username=obj.user.user.username).values_list("user__username", flat=True).first()
        user = Votes.objects.filter(user__user__username=obj.user.user.username).values_list("user__user__username", flat=True).first() 
        return user
        
        """
    def get_post(self, obj):
        p = Posts.objects.filter(image__id=obj.image)
        print(p)
        #p = Posts.objects.filter()
        """      
              
class DetailSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.user.username")
    #comments = CommentsSerializer(many=True)
    #votes = VotesSerializer(many=True)
    comments_count = serializers.SerializerMethodField()
    vote_of_post_owner = serializers.SerializerMethodField()
    #all_votes = serializers.SerializerMethodField()
    #comments = serializers.SerializerMethodField()
    #comments =  CommentsSerializer(many=True)
    
    
    class Meta:
        model = Posts
        fields = ["id", "user", "comments_count", "vote_of_post_owner"]
        #all_votes, "comments"


    def get_comments_count(self, obj):
        print(obj.image)
        c_count = Comments.objects.filter(image__image=obj.image).count()
        return c_count
    
    """
    def get_comments(self, obj):
        print(obj.image)
        get_comment = Comments.objects.filter(image__image=obj.image).values_list('message', flat=True)
        return get_comment"""
    
    
    def get_vote_of_post_owner(self, obj):
        if 'request' in self.context:
            #print(obj.user, "obj.user")
            #print(request.user, "request.user")
            request = self.context['request']
            user = request.user
            vote = Votes.objects.filter(user__user__username=user, image__image=obj.image).values_list("vote", flat=True).first()
            return vote
        else:
            print("no request avaliable in self.context")
            
        #total_votes, UP VOTES, DOWN VOTES can also be down here in with SerializerMethodField (Custom Serializer Field)
    """
    def get_all_votes(self, data):
        print(data, "data")
        print(dir(data))
        id = data.id
        total_vote = Votes.objects.filter(image__id=id).values_list ("vote", flat=True)
        l = list(total_vote)
        votes_dict = {}
        votes_dict["total_votes"] = len(l)
        votes_dict["up_votes"] = l.count("UP")
        votes_dict["down_votes"] = l.count("DOWN")
        return votes_dict
    """