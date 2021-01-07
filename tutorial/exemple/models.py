from django.db import models
from django_countries.fields import CountryField
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User
from datetime import datetime


class Category(MPTTModel):
    name = models.CharField(max_length=50, verbose_name='Категория')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Author(models.Model):
    name = models.CharField("Имя автора", max_length=70)
    dob = models.DateField("Дата рождения", null=True)
    bpl = models.CharField("Место рождения", max_length=50, blank=True)
    dod = models.DateField("Дата смерти", null=True, blank=True)
    bio = models.TextField("Биография", max_length=500, null=True)
    citizenship = CountryField("Гражданство", blank_label='Страна', blank=True)
    category = TreeForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE, null=True)
    deleted = models.BooleanField(default=False, verbose_name='Удалено')
    delete_date = models.DateTimeField(blank=True, null=True, verbose_name='Дата удаления')
    who = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Кем удалено')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

    def delete(self, using=None, keep_parents=False):
        self.deleted = True
        self.save()

    def save(self, *args, **kwargs):
        if self.deleted:
            self.delete_date = datetime.now()
        elif not self.deleted and self.delete_date is not None:
            self.delete_date = None
        return super().save(*args, **kwargs)


class Book(models.Model):
    title = models.CharField("Название", max_length=120)
    pub_date = models.DateField("Дата публикации", null=True)
    description = models.TextField("Описание", max_length=1000)
    author = models.ForeignKey(Author, verbose_name='Автор', null=True, on_delete=models.SET_NULL)
    category = TreeForeignKey(Category, verbose_name='Категория', null=True, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False, verbose_name='Удалено')
    delete_date = models.DateTimeField(blank=True, null=True, verbose_name='Дата удаления')
    who = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Кем удалено')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

    def delete(self, using=None, keep_parents=False):
        self.deleted = True
        self.save()

    def save(self, *args, **kwargs):
        if self.deleted:
            self.delete_date = datetime.now()
        elif not self.deleted and self.delete_date is not None:
            self.delete_date = None
        return super().save(*args, **kwargs)