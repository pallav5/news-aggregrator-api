from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password



class HeadlineSerializer(serializers.ModelSerializer):
    topic = serializers.CharField(source="topic.title", read_only=True)
    topic_id = serializers.CharField(source="topic.id", read_only=True)
    class Meta:

        model = Headline
        fields = ('topic','title','image','url','topic_id')



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class TopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic
        fields = ('subscriber','title',)



class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)


    def validate_email(self,usernname):
        if User.objects.filter(username = usernname).exists():
            raise serializers.ValidationError("email already exists")
        return usernname

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        if User.objects.filter(username = username).exists():
            raise serializers.ValidationError({'fail': 'email already exists'})

        else:
            user = User.objects.create_user(
                username=username,
                email=email,
            )
            user.set_password(validated_data['password1'])
            user.save()


            return validated_data
