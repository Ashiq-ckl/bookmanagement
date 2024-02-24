from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .. models import Book
from .. serializers.review import ReviewListSerializer

def field_length(fieldname):
    field = next(field for field in Book._meta.fields if field.name == fieldname)
    return field.max_length

class BookCreateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True,max_length=field_length('name'),validators=[UniqueValidator(queryset=Book.objects.all(),message='Book name already exists.')],error_messages={'required':'Book name is required'})

    def save(self, **kwargs):
        book = Book.objects.create(**self.validated_data)
        return book
    
class BookListSerializer(serializers.Serializer):
    name = serializers.CharField(read_only=True)
    review = ReviewListSerializer(source='book_review',many=True)
    assigned_by = serializers.SerializerMethodField(read_only=True)

    def get_assigned_by(self,obj):
        rec = list(obj.author)
        if len(rec) > 0:
            return rec[0].author.name