"""This module defines admin panel."""
from django.contrib import admin

from .models import Filmwork, Genre, GenreFilmwork, Person, PersonFilmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """This class defines field with genres in admin panel."""

    list_display = ('name', 'description',)

    search_fields = ('name', 'description', 'id',)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    """This class defines field with persons in admin panel."""

    list_display = ('full_name',)

    search_fields = ('full_name', 'id',)


class GenreFilmworkInline(admin.TabularInline,):
    """This class defines connection movies with genres in admin panel."""

    model = GenreFilmwork


class PersonFilmworkInline(admin.TabularInline,):
    """This class defines connection movies with persons in admin panel."""

    model = PersonFilmwork


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    """This class defines field with movies in admin panel."""

    inlines = (GenreFilmworkInline, PersonFilmworkInline)

    list_display = ('title', 'type', 'creation_date', 'rating', 'mpaa_rating')

    list_filter = ('type',)

    search_fields = ('title', 'description', 'id',)
