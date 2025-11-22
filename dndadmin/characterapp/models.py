from django.contrib.auth import get_user, get_user_model
from django.db import models

from bookdata.models import DndClass, Race, Background


class Character(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    dnd_class = models.ForeignKey(DndClass, on_delete=models.PROTECT, null=True, verbose_name="Класс")
    race = models.ForeignKey(Race, on_delete=models.PROTECT, null=True, verbose_name="Раса")
    background = models.ForeignKey(Background, on_delete=models.PROTECT, null=True, verbose_name="Предыстория")
    max_hp = models.IntegerField(default=0, verbose_name="Max hp")
    hp = models.IntegerField(default=0, verbose_name="HP")
    armor_class = models.IntegerField(default=0, verbose_name="КД")
    initiative = models.IntegerField(null=True, verbose_name="Инициатива")
    cooper_coins = models.IntegerField(default=0, verbose_name="ММ")
    silver_coins = models.IntegerField(default=0, verbose_name="СМ")
    gold_coins = models.IntegerField(default=0, verbose_name="ЗМ")
    is_player = models.BooleanField(verbose_name="Игрок")
    player_name = models.CharField(max_length=100, null=True, verbose_name="Имя игрока")
    image = models.ImageField(upload_to="characters/", null=True, blank=True, verbose_name="Изображение")
    user = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.PROTECT)
    level = models.IntegerField(default=1, verbose_name="Уровень")

    class Meta:
        verbose_name = "Персонаж"
        verbose_name_plural = "Персонажи"

    def __str__(self):
        return self.name



class Ability(models.Model):

    class AbilityType(models.TextChoices):
        STR = 'STR', 'Сила'
        DEX = 'DEX', 'Ловкость'
        CON = 'CON', 'Телосложение'
        INT = 'INT', 'Интелект'
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


