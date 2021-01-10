from mptt.admin import MPTTModelAdmin
from .models import Category, Author, Book
from django.contrib import admin


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    mptt_level_indent = 40
    list_display = ('name',)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'deleted', 'deleted_at', 'deleted_by')
    list_display_links = ('name', 'category',)
    list_editable = ("deleted",)
    search_fields = ('name', 'category__name')
    list_filter = ('name', 'category', ('deleted', admin.BooleanFieldListFilter))
    fieldsets = [
        ('Информация', {'fields': ('name', 'dob', 'dod', 'citizenship', 'bpl', 'bio', 'category', 'books')})
    ]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'deleted', 'deleted_at', 'deleted_by')
    list_display_links = ('title', 'author',)
    list_editable = ("deleted",)
    search_fields = ('title', 'category__name')
    list_filter = ('title', 'category', ('deleted', admin.BooleanFieldListFilter))
    fieldsets = [
        ('Информация', {'fields': ('title', 'description', 'author', 'pub_date', 'category')})
    ]


