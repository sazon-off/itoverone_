from django.db import models
from django_countries.fields import CountryField
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User


class Category(MPTTModel):
    name = models.CharField(max_length=50, verbose_name='Категория')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, default=40, related_name='subcategory')

    def __str__(self):
        return self.name

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by = ['name']

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Book(models.Model):
    title = models.CharField("Название", max_length=120)
    pub_date = models.DateField("Дата публикации", null=True)
    description = models.TextField("Описание", max_length=1000)
    author = models.ForeignKey("Author", verbose_name='Автор', null=True, on_delete=models.SET_NULL)
    category = TreeForeignKey(Category, verbose_name='Категория', null=True, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False, verbose_name='Удалено')
    deleted_at = models.DateTimeField(blank=True, null=True, verbose_name='Дата удаления')
    deleted_by = models.ForeignKey(User, default=None, blank=True, null=True, on_delete=models.DO_NOTHING,
                                   verbose_name='Удалил')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

    def save(self, *args, **kwargs):
        if not self.deleted and self.deleted_at is not None:
            self.deleted_at = None
            self.deleted_by = None
        return super().save(*args, **kwargs)


class Author(models.Model):
    name = models.CharField("Имя автора", max_length=70)
    dob = models.DateField("Дата рождения", null=True)
    bpl = models.CharField("Место рождения", max_length=50, blank=True)
    dod = models.DateField("Дата смерти", null=True, blank=True)
    bio = models.TextField("Биография", max_length=500, null=True)
    citizenship = CountryField("Гражданство", blank_label='Страна', blank=True)
    books = models.ManyToManyField(Book, verbose_name='Книги автора', blank=True, related_name='books')
    category = TreeForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE, null=True,
                              related_name='category')
    deleted = models.BooleanField(default=False, verbose_name='Удалено')
    deleted_at = models.DateTimeField(blank=True, null=True, verbose_name='Дата удаления')
    deleted_by = models.ForeignKey(User, default=None, blank=True, null=True, on_delete=models.DO_NOTHING,
                                   verbose_name='Удалил')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

    def save(self, *args, **kwargs):
        if not self.deleted and self.deleted_at is not None:
            self.deleted_at = None
            self.deleted_by = None
        return super().save(*args, **kwargs)