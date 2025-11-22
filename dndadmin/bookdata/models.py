from django.db import models

class DndClass(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    image = models.ImageField(upload_to="bookdata/classes/", null=True, blank=True, verbose_name="Изображение")

    class Meta:
        verbose_name = "Класс"
        verbose_name_plural = "Классы"

    def __str__(self):
        return self.name

class Race(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    image = models.ImageField(upload_to="bookdata/races/", null=True, blank=True, verbose_name="Изображение")

    class Meta:
        verbose_name = "Раса"
        verbose_name_plural = "Расы"

    def __str__(self):
        return self.name

class Background(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    image = models.ImageField(upload_to="bookdata/backgrounds/", null=True, blank=True, verbose_name="Изображение")

    class Meta:
        verbose_name = "Происхождение"
        verbose_name_plural = "Происхождения"

    def __str__(self):
        return self.name


