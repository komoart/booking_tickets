"""This module describes models of data."""
import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    """Class defines timestamp columns."""

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        """Makes abstract."""

        abstract = True


class UUIDMixin(models.Model):
    """Class defines id columns."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        """Makes abstract."""

        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    """Class defines Genre table."""

    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        """Parameters of psql table."""

        db_table = "content\".\"genre"
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        """Show name of genre.

        Returns:
            name of genre

        """
        return self.name


class Person(UUIDMixin, TimeStampedMixin):
    """Class defines Person table."""

    full_name = models.CharField(_('full name'), max_length=255)

    class Meta:
        """Parameters of psql table."""

        db_table = "content\".\"person"
        verbose_name = 'Человек'
        verbose_name_plural = 'Люди'

    def __str__(self):
        """Show full name of person.

        Returns:
            full name of person

        """
        return self.full_name


class Filmwork(UUIDMixin, TimeStampedMixin):
    """Class defines Person table."""

    title = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    creation_date = models.DateField(_('creation date'), blank=True)
    mpaa_rating = models.TextField(_('mpaa rating'), blank=True)
    rating = models.FloatField(
        _('rating'),
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    file_path = models.FileField(
        blank=True,
        null=True,
        upload_to='movies/',
        verbose_name=_('film_file_path'),
        help_text=_('film_file_path_help_text'),
    )

    class Type(models.TextChoices):
        """Class defines choice for type."""

        MOVIE = _('movie')
        TV_SHOW = _('tv-show')
    type = models.TextField(choices=Type.choices)
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    persons = models.ManyToManyField(Person, through='PersonFilmwork')

    class Meta:
        """Parameters of psql table."""

        db_table = "content\".\"film_work"
        verbose_name = 'Кинопроизведение'
        verbose_name_plural = 'Кинопроизведения'

    def __str__(self):
        """Show title of filmwork.

        Returns:
            title of filmwork

        """
        return self.title


class GenreFilmwork(UUIDMixin):
    """Class defines GenreFilmwork table."""

    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Parameters of psql table."""

        db_table = "content\".\"genre_film_work"
        unique_together = ['film_work', 'genre']


class PersonFilmwork(UUIDMixin):
    """Class defines PersonFilmwork table."""

    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.TextField(_('role'), null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Parameters of psql table."""

        db_table = "content\".\"person_film_work"
        unique_together = ['film_work', 'person', 'role']
