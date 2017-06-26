""" Instance Serializers
"""
from rest_framework_mongoengine.serializers import DocumentSerializer
from core_federated_search_app.components.instance.models import Instance


class InstanceSerializer(DocumentSerializer):
    """ Instance serializer
    """
    class Meta:
        """ Meta
        """
        model = Instance
        fields = "__all__"
