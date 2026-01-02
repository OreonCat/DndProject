from django.contrib.auth import get_user, get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django_extensions.db.fields import slugify
from transliterate import translit

from bookdata.models import DndClass, Race, Background


class Character(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    dnd_class = models.ForeignKey(DndClass, on_delete=models.PROTECT, null=True, verbose_name="Класс")
    dnd_subclass = models.CharField(max_length=100, verbose_name="Подкласс", null=True, blank=True)
    race = models.ForeignKey(Race, on_delete=models.PROTECT, null=True, verbose_name="Раса")
    background = models.ForeignKey(Background, on_delete=models.PROTECT, null=True, verbose_name="Предыстория")
    max_hp = models.IntegerField(default=0, verbose_name="Max hp", validators=[MinValueValidator(0)])
    hp = models.IntegerField(default=0, verbose_name="HP", validators=[MinValueValidator(0)])
    armor_class = models.IntegerField(default=0, verbose_name="КД", validators=[MinValueValidator(0)])
    initiative = models.IntegerField(null=True, verbose_name="Инициатива")
    cooper_coins = models.IntegerField(default=0, verbose_name="ММ", validators=[MinValueValidator(0)])
    silver_coins = models.IntegerField(default=0, verbose_name="СМ", validators=[MinValueValidator(0)])
    gold_coins = models.IntegerField(default=0, verbose_name="ЗМ", validators=[MinValueValidator(0)])
    is_player = models.BooleanField(verbose_name="Игрок")
    player_name = models.CharField(max_length=100, null=True, verbose_name="Имя игрока", blank=True)
    image = models.ImageField(upload_to="characters/", null=True, blank=True, verbose_name="Изображение")
    user = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.PROTECT)
    level = models.IntegerField(default=1, verbose_name="Уровень", validators=[MinValueValidator(1)])
    speed = models.IntegerField(default=0, verbose_name="Скорость", validators=[MinValueValidator(0)])
    proficient_bonus = models.IntegerField(default=2, verbose_name="Бонус мастерства")
    slug = models.SlugField(null=True, blank=True)

    class Meta:
        unique_together = ('name', 'race', 'user')
        verbose_name = "Персонаж"
        verbose_name_plural = "Персонажи"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('characters:character-detail', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('characters:character-update', kwargs={'pk': self.pk})

    def get_coin_update_url(self):
        return reverse('characters:coin-update', kwargs={'pk': self.pk})

    def get_go_to_gold_url(self):
        return reverse('characters:go-to-gold', kwargs={'pk': self.pk})

    def go_to_gold(self):
        temp = self.cooper_coins // 10
        self.cooper_coins = self.cooper_coins % 10
        self.silver_coins = self.silver_coins + temp
        temp = self.silver_coins // 10
        self.silver_coins = self.silver_coins % 10
        self.gold_coins = self.gold_coins + temp

    def save(self, *args, **kwargs):

        future_slug_raw = self.name + "_" + self.race.name + "_" + self.user.username
        future_slug = translit(future_slug_raw, 'ru', reversed=True)
        self.slug = slugify(future_slug)
        super().save(*args, **kwargs)



class Ability(models.Model):

    class AbilityType(models.TextChoices):
        STR = 'STR', 'Сила'
        DEX = 'DEX', 'Ловкость'
        CON = 'CON', 'Телосложение'
        INT = 'INT', 'Интеллект'
        WIS = 'WIS', 'Мудрость'
        CHR = 'CHR', 'Харизма'

    ability = models.CharField(max_length=3, choices=AbilityType.choices, verbose_name="Навык")
    value = models.IntegerField(default=0, verbose_name="Характеристика")
    is_proficient = models.BooleanField(verbose_name="Профильное", default=False)
    character = models.ForeignKey(Character, on_delete=models.PROTECT, verbose_name="Персонаж", related_name="abilities")
    saving_throw = models.IntegerField(default=0, verbose_name="Спас бросок")


    class Meta:
        unique_together = ('character', 'ability')
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"

    def __str__(self):
        return f"{self.character.name} {self.get_ability_display()}"

class Skill(models.Model):
    class SkillType(models.TextChoices):
        ATH = 'ATH', 'Атлетика'
        ACR = 'ACR', 'Акробатика'
        SOH = 'SOH', 'Ловкость рук'
        STL = 'STL', 'Скрытность'
        ARC = 'ARC', 'Магия'
        HIS = 'HIS', 'История'
        INV = 'INV', 'Анализ'
        NAT = 'NAT', 'Природа'
        REL = 'REL', 'Религия'
        ANH = 'ANH', 'Уход за животными'
        INS = 'INS', 'Проницательность'
        MED = 'MED', 'Медицина'
        PER = 'PER', 'Восприятие'
        SUR = 'SUR', 'Выживание'
        DEC = 'DEC', 'Обман'
        IND = 'IND', 'Запугивание'
        PRF = 'PRF', 'Выступление'
        PRS = 'PRS', 'Убеждение'

    skill = models.CharField(max_length=3, choices=SkillType.choices, verbose_name="Скилл")
    value = models.IntegerField(default=0, verbose_name="Характеристика")
    is_proficient = models.BooleanField(verbose_name="Профильное", default=False)
    ability = models.ForeignKey(Ability, on_delete=models.PROTECT, verbose_name="Навык", related_name="skills")

    class Meta:
        unique_together = ('ability', 'skill')
        verbose_name = "Скилл"
        verbose_name_plural = "Скиллы"

    @classmethod
    def create_skills(cls, ability:Ability):
        if ability.ability == 'STR':
            Skill.objects.create(ability=ability, skill=Skill.SkillType.ATH).save()
        elif ability.ability == 'DEX':
            Skill.objects.create(ability=ability, skill=Skill.SkillType.ACR).save()
            Skill.objects.create(ability=ability, skill=Skill.SkillType.SOH).save()
            Skill.objects.create(ability=ability, skill=Skill.SkillType.STL).save()
        elif ability.ability == 'INT':
            Skill.objects.create(ability=ability, skill=Skill.SkillType.ARC).save()
            Skill.objects.create(ability=ability, skill=Skill.SkillType.HIS).save()
            Skill.objects.create(ability=ability, skill=Skill.SkillType.INV).save()
            Skill.objects.create(ability=ability, skill=Skill.SkillType.NAT).save()
            Skill.objects.create(ability=ability, skill=Skill.SkillType.REL).save()
        elif ability.ability == 'WIS':
            Skill.objects.create(ability=ability, skill=Skill.SkillType.ANH).save()
            Skill.objects.create(ability=ability, skill=Skill.SkillType.INS).save()
            Skill.objects.create(ability=ability, skill=Skill.SkillType.MED).save()
            Skill.objects.create(ability=ability, skill=Skill.SkillType.PER).save()
            Skill.objects.create(ability=ability, skill=Skill.SkillType.SUR).save()
        elif ability.ability == 'CHR':
            Skill.objects.create(ability=ability, skill=Skill.SkillType.DEC).save()
            Skill.objects.create(ability=ability, skill=Skill.SkillType.IND).save()
            Skill.objects.create(ability=ability, skill=Skill.SkillType.PRF).save()
            Skill.objects.create(ability=ability, skill=Skill.SkillType.PRS).save()


