from django.db import IntegrityError

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .. models import Author,Book,Review

def field_length(fieldname):
    field = next(field for field in Review._meta.fields if field.name == fieldname)
    return field.max_length

class ReviewCreateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True,max_length=field_length('name'),error_messages={'required':'Name is required'})
    book = serializers.PrimaryKeyRelatedField(required=False,queryset=Book.objects.all(),error_messages = {'does_not_exist':'Book is not valid'})
    author = serializers.PrimaryKeyRelatedField(required=False,queryset=Author.objects.all(),error_messages = {'does_not_exist':'Author is not valid'})
    review = serializers.CharField(error_messages={'required':'Review is required'})
    def validate(self, attrs):
        if 'book' not in attrs.keys() and 'author' not in attrs.keys():
            raise serializers.ValidationError({'message':'Please select book or author.'})
        
        return super().validate(attrs)
    def save(self, **kwargs):
        author = Review.objects.create(**self.validated_data)
        return author
    
class ReviewListSerializer(serializers.Serializer):
    name = serializers.CharField(read_only=True)
    review = serializers.CharField(read_only=True)