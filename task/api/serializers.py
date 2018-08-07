from rest_framework import serializers
from task.models import Group, Element, models


class ElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Element
        fields = ('id',
                  'name',
                  'description',
                  'url',
                  'created',
                  'image',
                  'check_by_moderator',
                   'group')
        extra_kwargs = {
            'id': {'read_only': True},
            'created': {'read_only': True},
            'check_by_moderator':{'read_only': True}
        }


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id',
                  'name',
                  'description',
                  'url',
                  'image',
                  'parent',
                  'number_of_elements',
                  'number_of_children',
                  'elements')
        extra_kwargs = {
            'id': {'read_only': True},
            'number_of_elements': {'read_only': True},
            'number_of_children': {'read_only': True}
        }



# from rest_framework import serializers
#
# from .models import User, Post, Photo
#
#
# class UserSerializer(serializers.ModelSerializer):
#     posts = serializers.HyperlinkedIdentityField('posts', view_name='userpost-list', lookup_field='username')
#
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'first_name', 'last_name', 'posts', )