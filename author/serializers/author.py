from django.db import IntegrityError

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .. models import Author,Book,AuthorBook
from ..validators import validate_possible_number,FileValidator
from ..costantvariables import ALLOWED_FILE_SIZE,ALLOWED_EXTENSION 
from ..serializers.review import ReviewListSerializer

def field_length(fieldname):
    field = next(field for field in Author._meta.fields if field.name == fieldname)
    return field.max_length

class AuthorCreateSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True,max_length=field_length('first_name'),error_messages={'required':'First name is required'})
    last_name = serializers.CharField(required=True,max_length=field_length('last_name'),error_messages={'required':'Last name is required'})
    phone = serializers.CharField(validators=[validate_possible_number,UniqueValidator(queryset=Author.objects.all(),message='Mobile number already exists with another author')],error_messages={'required':'Mobile Number is required'})
    image = serializers.FileField(validators=[FileValidator(max_size=ALLOWED_FILE_SIZE,allowed_extensions=ALLOWED_EXTENSION)],error_messages = {'required':'Image is required'})
    rating = serializers.IntegerField(min_value=0, max_value=5)
    def save(self, **kwargs):
        author = Author.objects.create(**self.validated_data)
        return author

class AssignedBooksListSerializer(serializers.Serializer):
    created_at = serializers.DateTimeField(format='%Y-%m-%d %I:%M:%S')
    book = serializers.CharField(source='book.name',read_only=True)

class AuthorListSerializer(serializers.Serializer):
    name = serializers.CharField(read_only=True)
    phone = serializers.CharField(read_only=True)
    image = serializers.SerializerMethodField(read_only=True)
    rating = serializers.IntegerField()
    assigned_books_count = serializers.IntegerField()
    assigned_books = AssignedBooksListSerializer(source='author',many=True)
    review_count = serializers.IntegerField()
    review = ReviewListSerializer(source='author_review',many=True)

    def get_image(self,obj):
        request = self.context['request']
        return request.build_absolute_uri(obj.image.url)
    
class AssignBookSerializer(serializers.Serializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(),validators=[UniqueValidator(queryset=AuthorBook.objects.all(),message='Book assigned already.')],error_messages = {'required':'Book is required','does_not_exist':'Book is not valid'})

    def validate(self, attrs):
        try:
            Author.objects.get(id=self.context['id'])
        except Author.DoesNotExist:
            raise serializers.ValidationError({'message':'Author is not valid.'})
        return super().validate(attrs)
    
    def save(self, **kwargs):
        try:
            data = self.validated_data
            data['author_id'] = self.context['id']
            obj = AuthorBook.objects.create(**data)
            return obj
        except IntegrityError:
            raise serializers.ValidationError({'result':'failure','message':'Book assigned already.'})
        
