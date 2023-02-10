from rest_framework import serializers
from applications.post.models import Post

class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    
    class Meta:
        model = Post
        fields = '__all__'

    # def to_representation(self, instance):
    #     # print(instance)
    #     representation =  super().to_representation(instance)
    #     # print(representation)
    #     representation['owner'] = instance.owner.email
    #     return representation

    # # def create(self, validated_data):
    # #     validated_data['owner'] = self.context['request'].user 
    # #     return super().create(validated_data)