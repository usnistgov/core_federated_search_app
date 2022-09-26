""" Instance Serializers
"""
from rest_framework.fields import CharField, IntegerField
from rest_framework.serializers import ModelSerializer

import core_federated_search_app.components.instance.api as instance_api
from core_federated_search_app.components.instance.models import Instance


class InstanceSerializerModel(ModelSerializer):
    """Instance serializer"""

    class Meta:
        """Meta"""

        model = Instance
        fields = "__all__"
        read_only_fields = (
            "endpoint",
            "access_token",
            "refresh_token",
            "expires",
        )

    def create(self, validated_data):
        raise Exception("Wrong serializer for creation")

    def update(self, instance, validated_data):
        # The only field we can actually update is the name of the instance
        instance.name = validated_data.get("name", instance.name)
        return instance_api.upsert(instance)


class InstanceSerializerCreate(ModelSerializer):
    """Instance serializer for post method"""

    client_id = CharField()
    client_secret = CharField()
    timeout = IntegerField()
    username = CharField()
    password = CharField()

    class Meta:
        """Meta"""

        model = Instance
        fields = [
            "name",
            "endpoint",
            "client_id",
            "client_secret",
            "timeout",
            "username",
            "password",
        ]

    def create(self, validated_data):
        # return an instance after request the access token
        return instance_api.add_instance(**validated_data)

    def update(self, instance, validated_data):
        raise Exception("Wrong serializer for update")
