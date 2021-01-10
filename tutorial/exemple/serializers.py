from rest_framework import serializers
from .models import Book, Author, Category


class RecursiveField(serializers.ModelSerializer):

    def to_representation(self, value):
        parent_serializer = self.parent.parent.__class__
        serializer = parent_serializer(value, context=self.context)
        return serializer.data


class CategorySerializer(serializers.ModelSerializer):
    subcategory = RecursiveField(many=True, read_only=True)

    def create(self, validated_data):
        category, created = Category.objects.update_or_create(
            name=validated_data.get('name', None),
            defaults={'name': validated_data.get('name', None)})
        return category

    class Meta:
        model = Category
        fields = ('id', 'name', 'subcategory')


class AuthorListSerializer(serializers.ModelSerializer):
    category = serializers.CharField(write_only=True, label='Категория')

    def validate(self, data):
        try:
            data['category'] = Category.objects.get(name=data['category'])
        except:
            data['category'] = Category.objects.create(name=data['category'])

        return data

    class Meta:
        model = Author
        exclude = ("deleted", "deleted_by", "deleted_at")
        extra_kwargs = {

            'citizenship': {'write_only': True},
            'dob': {'write_only': True},
            'dod': {'write_only': True},
            'bpl': {'write_only': True},
            'bio': {'write_only': True},
            'category': {'write_only': True},
            'books': {'write_only': True},
        }


class AuthorDetailSerializer(serializers.ModelSerializer):
    books = serializers.SlugRelatedField(read_only=True, slug_field='title', many=True)
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all(), label='Категория')

    class Meta:
        model = Author
        exclude = ("deleted", "deleted_by", "deleted_at")


class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('title',)


class BookListSerializer(serializers.ModelSerializer):
    category = serializers.CharField(label='Категория')
    author = serializers.SlugRelatedField(slug_field='name', label='Автор', queryset=Author.objects.all())

    def validate(self, data):
        try:
            data['category'] = Category.objects.get(name=data['category'])
        except:
            data['category'] = Category.objects.create(name=data['category'])

        return data

    class Meta:
        model = Book
        exclude = ("deleted", "deleted_by", "deleted_at")
        extra_kwargs = {

            'pub_date': {'write_only': True},
            'description': {'write_only': True},
        }


class BookDetailSerializer(serializers.ModelSerializer):
    category = serializers.CharField(label='Категория')
    author = serializers.SlugRelatedField(slug_field='name', label='Автор', queryset=Author.objects.all(), )

    class Meta:
        model = Book
        exclude = ("deleted", "deleted_by", "deleted_at")