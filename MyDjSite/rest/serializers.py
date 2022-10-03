from rest.models import Breed, Cat
from rest_framework import serializers

class BreedSerializer(serializers.ModelSerializer):
    cats = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Breed
        fields = ( 'name', 'cats')

class CatSerializer(serializers.ModelSerializer):

    breed = serializers.SlugRelatedField(queryset=Breed.objects.all(), slug_field='name')

    class Meta:
        model = Cat
        fields = ( 'nickname', 'weight', 'foods', 'breed')

    