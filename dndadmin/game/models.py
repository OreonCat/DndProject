from datetime import timezone, datetime

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

    def check_master(self, user):
        return self.master == user


class Encounter(models.Model):
    stage = models.IntegerField(validators=[MinValueValidator(0)], default=0, verbose_name="Ход")
    is_start = models.BooleanField(default=False, verbose_name="Начат")
    is_complete = models.BooleanField(default=False, verbose_name="Завершен")
    game = models.ForeignKey(Game, related_name='encounters', on_delete=models.CASCADE, verbose_name="Игра")
    time_start = models.DateTimeField(auto_now_add=True, verbose_name="Время начала")
    time_end = models.DateTimeField(null=True, blank=True, verbose_name="Время окончания")

    class Meta:
        verbose_name = "Битва"
        verbose_name_plural = "Битвы"
        ordering = ['is_complete', '-time_start']

    def get_absolute_url(self):
        return reverse('game:encounter-detail', kwargs={'pk': self.pk})

    def get_start_url(self):
        return reverse('game:encounter-start', kwargs={'pk': self.pk})

    def get_next_url(self):
        return reverse('game:encounter-next-step', kwargs={'pk': self.pk})

    def get_close_url(self):
        return reverse('game:encounter-close', kwargs={'pk': self.pk})

    def start(self):
        self.stage = 1
        self.is_start = True
        self.save()

        characters = self.encounter_characters.all().order_by('-initiative')
        character = characters[0]
        character.make_step()

    def next_step(self):
        characters = self.encounter_characters.all().order_by('-initiative')
        for i in range(0, len(characters)):
            next_step = i+1
            if characters[i].is_my_step and next_step < len(characters):
                characters[i].end_step()
                characters[i+1].make_step()
                break
            elif characters[i].is_my_step:
                characters[i].end_step()
                characters[0].make_step()
                self.stage += 1
                self.save()
                break

    def close_encounter(self):
        self.is_complete = True
        self.time_end = datetime.now()
        characters = self.encounter_characters.all().order_by('-initiative')
        for character in characters:
            if character.is_my_step:
                character.end_step()
            if character.character.is_player:
                character.character.hp = character.hp
                character.character.save()
        self.save()


class EncounterCharacter(models.Model):
    character = models.ForeignKey(Character, verbose_name="Персонаж", on_delete=models.PROTECT, related_name="encounters")
    encounter = models.ForeignKey(Encounter, on_delete=models.CASCADE, verbose_name="Бой", related_name="encounter_characters")
    is_enemy = models.BooleanField(default=False, verbose_name="Противник")
    initiative = models.IntegerField(default=0)
    is_my_step = models.BooleanField(default=False)
    hp = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    max_hp = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    class Meta:
        verbose_name = "Участник битвы"
        verbose_name_plural = "Участники битвы"


    def delete_from_encounter(self):
        return reverse('game:encounter-delete-character', kwargs={'encounter_id': self.encounter.pk, 'pk': self.pk})

    def get_damage_url(self):
        return reverse('game:encounter-character-get-damage', kwargs={'pk': self.pk})

    def get_health_url(self):
        return reverse('game:encounter-character-get-health', kwargs={'pk': self.pk})

    def set_initiative(self, initiative):
        self.initiative = initiative + self.character.initiative
        self.save()

    def get_initiative_url(self):
        return reverse('game:encounter-character-get-initiative', kwargs={'pk': self.pk})

    def make_step(self):
        self.is_my_step = True
        self.save()

    def end_step(self):
        self.is_my_step = False
        self.save()

    def make_damage(self, damage):
        if self.hp - damage >= 0:
            self.hp -= damage
        else:
            self.hp = 0
        self.save()

    def make_health(self, health):
        if self.hp + health <= self.max_hp:
            self.hp += health
        else:
            self.hp = self.max_hp
        self.save()
