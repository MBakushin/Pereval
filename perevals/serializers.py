from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from config.settings import DATETIME_FORMAT
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'fam', 'name', 'otc', 'phone', ]


class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = ['latitude', 'longitude', 'height', ]


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['winter', 'summer', 'autumn', 'spring', ]


class ImagesSerializer(serializers.ModelSerializer):
    data = serializers.URLField()
    class Meta:
        model = Images
        fields = ['data', 'title', ]


class PerevalSerializer(WritableNestedModelSerializer):
    add_time = serializers.DateTimeField(format=DATETIME_FORMAT, read_only=True)
    status = serializers.HiddenField(default='NW')

    user = UserSerializer()
    coords = CoordsSerializer()
    level = LevelSerializer(allow_null=True)
    images = ImagesSerializer(many=True)

    class Meta:
        model = Pereval
        fields = ['id', 'status', 'beauty_title', 'title', 'other_title',
                  'connect', 'add_time', 'user', 'coords', 'level', 'images', ]

    def create(self, validated_data, **kwargs):
        user = validated_data.pop('user')
        coords = validated_data.pop('coords')
        level = validated_data.pop('level')
        images = validated_data.pop('images')

        user, created = User.objects.get_or_create(**user)

        coords = Coords.objects.create(**coords)
        level = Level.objects.create(**level)

        pereval = Pereval.objects.create(**validated_data, user=user,
                                         coords=coords, level=level)

        for i in images:
            data = i.pop('data')
            title = i.pop('title')
            Images.objects.create(data=data, title=title, pereval=pereval)

        return pereval

    def validate(self, data):
        if self.instance is not None:
            instance_user = self.instance.user
            data_user = data.get('user')
            validating_data_fields = [
                instance_user.email != data_user['email'],
                instance_user.fam != data_user['fam'],
                instance_user.name != data_user['name'],
                instance_user.otc != data_user['otc'],
                instance_user.phone != data_user['phone'],
            ]
            if data_user is not None and any(validating_data_fields):
                raise serializers.ValidationError({"Rejected": "User's data cannot be changed"})
        return data
