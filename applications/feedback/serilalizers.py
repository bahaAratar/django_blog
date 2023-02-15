from rest_framework import serializers
from .models import *

class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = '__all__'

class RatingSerilaizer(serializers.ModelSerializer):
    rating = serializers.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Rating
        fields = ('rating',)