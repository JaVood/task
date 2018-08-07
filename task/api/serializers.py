from rest_framework import serializers
from task.models import Group, Element


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
            'check_by_moderator': {'read_only': True}
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
