from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.HyperlinkedRelatedField(
        view_name = 'user-detail',
        read_only = True
    )

    snippets = serializers.HyperlinkedRelatedField(
        many = True,
        view_name = 'snippet-detail',
        read_only = True
    )

    primary_editor = serializers.HyperlinkedRelatedField(
        view_name = 'editor-detail',
        read_only = True
    )

    class Meta:
        model = Project
        fields = [
            'url', 'id', 'title', 'description', 'owner', 'snippets', 'primary_editor',
            'created', 'updated'
        ]