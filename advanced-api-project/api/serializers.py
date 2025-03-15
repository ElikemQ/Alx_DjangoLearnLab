from rest_framework import serializers
from .models import Author, Book
from datetime import datetime

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
# the serializer serializes the the model Book with all its fields (title, publication_year and author)

    def validate_publication_year(self, value):
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError
        return value
#the custom validation makes sure the publication year is not a date further than the present date. An error will occur if that happens  

    
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['name', 'books']

# the Author model is been serialized this serializer with the fields name and books