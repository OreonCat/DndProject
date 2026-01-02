from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse

from characterapp.models import Character

class Game(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True, verbose_name="Название")
    image = models.ImageField(upload_to='games/', null=True, blank=True, verbose_name="Изображение")
    characters = models.ManyToManyField(Character, verbose_name="Игроки", related_name="games")
    is_complete = models.BooleanField(default=False, verbose_name="Завершена")
    time_start = models.DateTimeField(auto_now_add=True, verbose_name="Время начала")
    time_end = models.DateTimeField(null=True, blank=True, verbose_name="Время окончания")
    master = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Мастер")

    class Meta:
        verbose_name = "Игра"
        verbose_name_plural = "Игры"

    def get_absolute_url(self):
        return reverse('game:game-detail', kwargs={'pk': self.pk})


class Encounter(models.Model):
    characters = models.ManyToManyField(Character, blank=True, related_name='encounters', verbose_name="Персонажи")
    stage = models.IntegerField(validators=[MinValueValidator(0)], default=0, verbose_name="Ход")
    enemies = models.ManyToManyField(Character, blank=True, related_name='encounters_enemy', verbose_name="Враги")
    is_complete = models.BooleanField(default=False, verbose_name="Завершен")
    game = models.ForeignKey(Game, related_name='encounters', on_delete=models.CASCADE, verbose_name="Игра")
    time_start = models.DateTimeField(auto_now_add=True, verbose_name="Время начала")
    time_end = models.DateTimeField(null=True, blank=True, verbose_name="Время окончания")

    class Meta:
        verbose_name = "Битва"
        verbose_name_plural = "Битвы"

    def get_absolute_url(self):
        return reverse('game:encounter-detail', kwargs={'pk': self.pk})