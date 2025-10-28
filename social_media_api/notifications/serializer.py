from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.StringRelatedField()       # shows username instead of id
    recipient = serializers.StringRelatedField()   # same here
    target = serializers.SerializerMethodField()   # to show what object was liked/commented

    class Meta:
        model = Notification
        fields = ['recipient', 'actor', 'verb', 'timestamp', 'target']

    def get_target(self, obj):
        if obj.target:
            return {'id': obj.object_id, 'repr': str(obj.target)}
        return None