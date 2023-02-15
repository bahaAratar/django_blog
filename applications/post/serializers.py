from ..post.models import *
from ..feedback.models import *
from ..feedback.serilalizers import LikeSerializer
from django.db.models import Avg
from rest_framework import serializers

class PostImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostImage
        fields = '__all__'
        # exclude = ('post',)

class PostSerializer(serializers.ModelSerializer):
    images = PostImageSerializer(many=True, read_only=True)
    owner = serializers.ReadOnlyField(source='owner.email')
    likes = LikeSerializer(many=True, read_only=True)

    # likes_count = serializers.SerializerMethodField()

    # def get_likes_count(self, post):
    #     return Like.objects.filter(post_id=post).count()

    class Meta:
        model = Post
        fields = '__all__'
        

    def to_representation(self, instance):
        representation =  super().to_representation(instance)

        representation['likes_count'] = instance.likes.filter(is_like=True).count()
        for like in representation['likes']:
            if not like['is_like']:
                representation['likes'].remove(like)

        # rating_result = 0
        # for i in instance.ratings.all():
        #     rating_result += i.rating
        # if rating_result:
        #     representation['rating'] = rating_result / instance.ratings.all().count()
        # else:
        #     representation['rating'] = rating_result
        representation['rating'] = instance.ratings.all().aggregate(Avg('rating'))['rating__avg']

        return representation

    # # def create(self, validated_data):
    # #     validated_data['owner'] = self.context['request'].user 
    # #     return super().create(validated_data)

    def create(self, validated_data):
        post = Post.objects.create(**validated_data)

        request = self.context.get('request')
        data = request.FILES
        # for i in data.getlist('images'):
        #     PostImage.objects.create(post=post, image=i)

        image_obj = []
        for i in data.getlist('images'):
            image_obj.append(PostImage(post=post, image=i))
        # print(image_obj)
        PostImage.objects.bulk_create(image_obj)

        return post

class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Comment
        fields = '__all__'
