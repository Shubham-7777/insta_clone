
from email import message
from functools import partial
from re import L
from xml.etree.ElementTree import Comment
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
import uuid

from django.shortcuts import render
from posts.models import Votes as VoteModel, Comments as CommentModel, Posts as PostModel
from posts.serializers import CommentsSerializer, PostsSerializer, VotesSerializer, DetailSerializer
from users.serializers import UserProfileSerializer
from users.models import UserProfile
# Create your views here.
from django.shortcuts import get_object_or_404
from django.db.models import Count



def get_logged_in_user(request):
    logged_in_user = UserProfile.objects.get(user__username=request.user)
    return logged_in_user    


def get_user_with_uuid(request):    
    get_uuid = UserProfile.objects.filter(user__username=request.user).values_list("code", flat=True).first()
    return get_uuid



class Posts(APIView):
    

    def get(self, request):
        user = request.user
        print(user, "user")
        logged_in_user = UserProfile.objects.get(user__username=user)
        following_users = logged_in_user.follow.following.all()
        post = PostModel.objects.filter(
            (Q(user__in=following_users) | 
            Q(user=logged_in_user)))#.order_by('-created_at')[:5]
        serializer = DetailSerializer(post, many=True, context = {"request" : request})
        serializer1 = UserProfileSerializer(logged_in_user)
        serialized_data = {"logged_in_user" : serializer1.data, "posts" : serializer.data}
        return Response(serialized_data, status=status.HTTP_200_OK)
    

                        

class PostsCreate(APIView):


    def post(self, request):
        images = request.FILES["image"]             
        # NOTE - with create ORM - cannot able to create a post - but direct request.data to serializer is working
        #user = UserProfile.objects.get(user__username=request.user)
        #create_post = PostModel.objects.create(user=user, image=images, caption=request.data["caption"]))
        #print(create_post, "create_post")
        #serializer = PostsSerializer(data=create_post, many=True)
        get_uuid = UserProfile.objects.filter(user__username=request.user).values_list("code", flat=True).first()
        request.data["user"] = get_uuid
        serializer = PostsSerializer(data=request.data)
        print(serializer.initial_data, "serializer.initial_data")
        # Example serializer.initial_data
        # serializer = MyFooSerializer(data={'foo':'bar'})
        # print(serializer.initial_data) # this will print {'foo':'bar'}
        if serializer.is_valid(raise_exception=True):
            print(serializer.validated_data, "serializer.validated_data")
            serializer.save()
            print(serializer.data, "serializer")
            return Response({"MESSAGE" : "POST created successfully"})
        #print(new_post)
        else:
            return Response({"ERROR" : serializer.errors, "MESSAGE" : "ERROR,  CANNOT created POST"})
            


    
class PostUpdateDelete(APIView):

    
    def get(self, request, id):
        print(id, "get_id_view")
        get_post = PostModel.objects.filter(user__user__username=request.user, id=id)
        if get_post.exists():
            serializer = PostsSerializer(get_post.first(), context = {"request" : request})
            detail_serializer = DetailSerializer(get_post.first(), context = {"request" : request})
            # also another way to add / update data into serializer
            total_vote = VoteModel.objects.filter(image__id=id).values_list ("vote", flat=True)
            l = list(total_vote)
            up, down, all = l.count("UP"), l.count("DOWN"), len(l)
            new_serializer = detail_serializer.data
            new_serializer["total_votes"] = all
            new_serializer["UP VOTES"] = up
            new_serializer["DOWN VOTES"] = down
            
            #comments 
            user_profile_serializer = UserProfileSerializer(get_logged_in_user(request))
            comments = CommentModel.objects.filter(image__id=id)
            commentserializer = CommentsSerializer(comments, many=True)
            return Response({"USER WHO POSTD DETAILS" : user_profile_serializer.data, "GET REQUEST SUCCESSFUL" : serializer.data, "IMAGE_DETAILS" :  new_serializer, "COMMENTS" : commentserializer.data}, status=status.HTTP_200_OK)   

        else:
            return Response({"MESSAGE" : "POST DOES NOT EXIST"}, status=status.HTTP_200_OK)   
                
    
    def put(self, request, id):
        print(id, "id")
        post = PostModel.objects.filter(user__user__username=request.user, id=id)
        print(post, "post")
        if post.exists():
            #get_uuid = UserProfile.objects.filter(user__username=request.user).values_list("code", flat=True).first()
            #print(get_uuid, "get_uuid")
            #print(get_user_with_uuid, dir(get_user_with_uuid), "get_user_with_uuid") 
            #value = get_user_with_uuid(request)
            #print(value)
            request.data["user"] = get_user_with_uuid(request)
            serializer = PostsSerializer(post.first(), data=request.data, context={'request': request})
            
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"MESSAGE" : serializer.data}, status=status.HTTP_200_OK)   
            else:
                return Response({"ERRORS" : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)   
        else:
            print("NOT EXIST")
            
                
    def delete(self, request, id):
        print(id)
        user_post = PostModel.objects.filter(id=id).values_list("user_id__user__username", flat=True).first()
        if user_post != request.user:
            return Response({"MESSAGE" : f"This POST is not owned by login user, login user - {request.user} > cannot delete {user_post} posts"}, status=status.HTTP_400_BAD_REQUEST)
        post_to_delete = PostModel.objects.filter(user__user__username=request.user, id=id)
        if post_to_delete.exists():
            post_to_delete.delete()            
            return Response({"MESSAGE" : "POST Deleted Successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"MESSAGE" : "POST does NOT exist or already deleted"}, status=status.HTTP_400_BAD_REQUEST)




class GetCommentImage(APIView):
    def get(self, request, post_id):
        user = get_logged_in_user(request)
        post = PostModel.objects.filter(id=post_id)
        comments = CommentModel.objects.filter(image__id=post_id)
        post = PostsSerializer(post.first())
        serializer =  CommentsSerializer(comments, many=True, context={'request': request})
        return Response({"POST" : post.data, "ALL COMMENTS" : serializer.data})


    def post(self, request, post_id):
        user = UserProfile.objects.get(user__username=request.user)
        post = PostModel.objects.get(id=post_id)
        comment = CommentModel.objects.create(user=user, image_id=post.id, message=request.data["message"])
        print(request.data)
        serializer_data = CommentsSerializer(comment, data=request.data, partial=True)
        if serializer_data.is_valid(raise_exception=True):
            serializer_data.save()
            print(serializer_data.initial_data, serializer_data.data)
            return Response({"MESSAGE" : "NEW COMMENT CREATED Successfully", "DATA" : serializer_data.data})
        else:
            return Response({"ERRORS"  : serializer_data.errors})


    # delete all comments of specific post by logged in user
    def delete(self, request, post_id):
        comments = CommentModel.objects.filter(user=get_logged_in_user(request), image__id=post_id)
        if comments.exists():
            comments.delete()
            return Response({"message" : "COMMENT DELETED SUCCESSFULLY"}, status=status.HTTP_200_OK)
        else:
            return Response({"message" : "COMMENT DOES NOT EXIST OR ALREADY DELETED"}, status=status.HTTP_400_BAD_REQUEST)
        


class CommentOnImage(APIView):
    
    
    def get(self, request, comment_id, post_id):
        user = get_logged_in_user(request)
        post = PostModel.objects.filter(id=post_id)
        comments = CommentModel.objects.filter(image__id=post_id, id=comment_id)
        post = PostsSerializer(post.first())
        serializer =  CommentsSerializer(comments.first(), context={'request': request})
        return Response({"POST_USER" : post.data, "COMMENT_DATA" : serializer.data})

    
        
    def put(self, request, comment_id, post_id):
        user = get_logged_in_user(request)
        comments = CommentModel.objects.filter(user=user, image__id=post_id, id=comment_id)
        #comments = CommentModel.objects.filter(user__user__username=request.user, image__id=post_id, id=comment_id)
        
        if comments.exists():
            post = PostModel.objects.filter(id=post_id)
            serializer =  CommentsSerializer(comments.first(), data=request.data, partial=True, context={'request': request})
            #serializer =  DetailSerializer(comments.first(), data=request.data, partial=True, context={'request': request})
            
            post = PostsSerializer(post.first())
            if serializer.is_valid(raise_exception=True):
                print(serializer.validated_data, "serializer.validated_data")
                print("VALID")
                serializer.save()
                return Response({"MESSAGE" : "COMMENT updated Successfully", "POST" : post.data, "COMMENT" : serializer.data})
            else:
                print("NOT VALID")
                return Response({"ERROR" : serializer.errors})
        else:
            print("OBJECT does NOT EXIST")
            return Response({"ERROR" : "OBJECT does NOT EXIST"})
    
    
    
    def delete(self, request, comment_id, post_id):
        comment = CommentModel.objects.filter(user=get_logged_in_user(request), image__id=post_id, id=comment_id)
        print(dir(comment))
        comment_c = CommentModel.objects.filter(image__id=post_id, id=comment_id).values_list("user__user__username", flat=True)
        if comment.exists():
            print("EXISTS")
            comment.first().delete()
            return Response({"message" : "COMMENT DELETED SUCCESSFULLY"}, status=status.HTTP_200_OK)
        elif comment_c.exists():
            print(" EXIST")
            comment_user = comment_c.first()
            return Response({"message" : f"COMMENT EXIST BUT CANNOT BE DELETED BY LOGGED IN USER login user > {request.user} comment owner > {comment_user}"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            print("NOT EXIST")
            return Response({"message" : "COMMENT DOES NOT EXIST OR ALREADY DELETED"}, status=status.HTTP_400_BAD_REQUEST)
        
    
    
    
class Votes(APIView):
    
    
    def get(self, request, post_id):
        post_to_vote = VoteModel.objects.filter(user=get_logged_in_user(request), image__id=post_id)
        vote = VoteModel.objects.filter(image__id=post_id)
        if post_to_vote.exists():
            print(post_to_vote, "post_to_vote")
            serializer = VotesSerializer(vote, many=True, context={'request': request})
            image_data = PostModel.objects.filter(id=post_id).first()
            image_serializer = PostsSerializer(image_data)
            print(serializer.data)
            return Response({"MESSAGE" : "GET successful POST request", "POST Serializer" : image_serializer.data, "VOTE Serializer" : serializer.data}, status=status.HTTP_200_OK)
        elif vote.exists(): 
            serializer = VotesSerializer(vote, many=True, context={'request': request})
            return Response({"MESSAGE" : "Post Does exist, BUT user have NOT voted in this Post", "VOTE Serializer" : serializer.data}, status=status.HTTP_200_OK)   
        else:    
            serializer = VotesSerializer(vote, many=True, context={'request': request})
            return Response({"MESSAGE" : "Post does NOT exist, SO cannot Vote", "VOTE Serializer" : serializer.data}, status=status.HTTP_400_BAD_REQUEST)



    def put(self, request, post_id):
        print(post_id)
        post_to_vote = VoteModel.objects.filter(user__user__username=request.user, image__id=post_id)
        print(post_to_vote)
        if post_to_vote.exists():
            print("exists")
            to_vote = VoteModel.objects.filter(user__user__username=request.user, image__id=post_id).first()
            get_vote = request.data["vote"]
            to_vote.vote = get_vote
            to_vote.save()
            serializer_data = VotesSerializer(to_vote, data=request.data, partial=True)
            if serializer_data.is_valid(raise_exception=True):
                serializer_data.save()
                print("VALID")
                return Response({"message" : "Vote updated as User already voted this image",
                                 "DATA" : serializer_data.data}, status=status.HTTP_200_OK)
            else:
                print("NOT VALID")
                return Response({"message" : "Serializer NOT VALID", "ERROR" : serializer_data.errors}, status=status.HTTP_400_BAD_REQUEST)
                
        else:
            print("new to create add vote first")
            # object does NOT exist so creating a new object
            print("NOT EXIST")
            get_vote = request.data["vote"]
            print(get_vote)
            l_user = UserProfile.objects.filter(user__username=request.user).first()
            post = PostModel.objects.filter(id=post_id).first()
            new_vote = VoteModel.objects.create(user=l_user, image=post, vote=get_vote)
            new_vote.save()
            serializer_data = VotesSerializer(new_vote, data=request.data, partial=True)
            if serializer_data.is_valid(raise_exception=True):
                print("VALID serializer new object")
                serializer_data.save()
                return Response({"message" : "Vote added - User voted this image first time", "DATA" : serializer_data.data}, status=status.HTTP_200_OK)
            else:
                print("NOT VALID")
                return Response({"message" : "Serializer NOT VALID on NEW OBJECT creation", "ERROR" : serializer_data.errors}, status=status.HTTP_400_BAD_REQUEST)
            


    def delete(self, request, post_id):
        #user = UserProfile.objects.filter(user__username=request.user).first()
        vote_delete = VoteModel.objects.filter(user=get_logged_in_user(request), image__id=post_id)
        if vote_delete.exists():
            print("EXISTS")
            vote_delete.first().delete()
            return Response({"message" : "VOTE DELETED SUCCESSFULLY"}, status=status.HTTP_200_OK)
            
        else:
            print("NOT EXISTS")
            return Response({"message" : "VOTE ALREADY DELETED OR DOES NOT EXIST"}, status=status.HTTP_400_BAD_REQUEST)
            
             

class SearchTags(APIView):
    
    
    def get(self, request, tag):
        tag_orm = PostModel.objects.filter(hashtags__tag__icontains=tag).distinct()
        if tag_orm.exists():
            serializer = PostsSerializer(tag_orm, many=True, context = {"request" : request})
            return Response({"SEARCH_DATA" : serializer.data})
        else:
            all = PostModel.objects.all()[:3]
            serializer = PostsSerializer(tag_orm, many=True, context = {"request" : request})
            return Response({"SEARCH_DATA" : serializer.data})
        
        
        
############################
#ERROR occuring in tne below  code 
###########################
"""     
    def put(self, request, post_id):
        print(post_id)
        get_post_to_vote  = PostModel.objects.filter(id=post_id).first()
        user = get_logged_in_user(request)
        post_to_vote = VoteModel.objects.filter(user__user__username=request.user, image=get_post_to_vote)#.values_list("vote", flat=True)
        print(post_to_vote, "post_to_vote")
        if post_to_vote.exists():
            print("asdadad")
            v = VoteModel.objects.filter(user__user__username=request.user, image__id=post_id).first()
            print(v, "v")
            vote = request.data.get("vote")
            v.vote = vote
            v.save()
            print("successful")
            print(request.data)
            serializer_data = VotesSerializer(data=request.data, partial=True)
            if serializer_data.is_valid(raise_exception=True):
            
                serializer_data.save()
                print("VALID")
                return Response({"message" : "Vote updated as User already voted this image",
                                 "DATA" : serializer_data.data}, status=status.HTTP_200_OK)
            else:
                print("NOT VALID")
                return Response({"message" : "ERROR", "ERROR" : serializer_data.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            print("new vote created")
            #vote = VoteModel.objects.create(user=user, image=get_post_to_vote, vote=vote)
            vote = VoteModel.objects.create(user__user__username=user, image__id=get_post_to_vote, vote=vote)
            
            vote.save()
            
            serializer_data = VotesSerializer(vote, data=request.data, partial=True)
            if serializer_data.is_valid(raise_exception=True):
                serializer_data.save()
                print("valid")
                return Response({"message" : "Vote added - User voted this image first time", "DATA" : serializer_data.data}, status=status.HTTP_200_OK)
            else:
                print("NOT VALID")
                return Response({"ERRORS" : serializer_data.errors}, status=status.HTTP_400_BAD_REQUEST)
"""

############################
#ERROR occuring in tne above code 
############################


def test(request):
    context = {"request" : request}
    template = "base.html"
    return render(request, template, context)




