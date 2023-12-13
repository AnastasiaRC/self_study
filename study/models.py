from django.db import models
from users.models import NULLABLE
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Topics(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    author = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Автор', **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'
        ordering = ('id',)

    def save(self, *args, **kwargs):
        """Валидация имени на уровне модели"""
        if not self.title[0].isupper():
            raise ValidationError(
                _('Название темы должно начинаться с заглавной буквы.'), )
        super().save(*args, **kwargs)


class Materials(models.Model):
    study_topic = models.ForeignKey(Topics, on_delete=models.CASCADE, verbose_name='Тема обучения')
    title = models.CharField(max_length=100, unique=True, verbose_name='Название')
    description = models.TextField(verbose_name='Содержание', **NULLABLE)
    author = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Автор', **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'
        ordering = ('id',)

    def save(self, *args, **kwargs):
        """Валидация имени на уровне модели"""
        if not self.title[0].isupper():
            raise ValidationError(
                _('Название материала должно начинаться с заглавной буквы.'),)
        super().save(*args, **kwargs)


class Questions(models.Model):
    item_materials = models.ForeignKey(Materials, on_delete=models.CASCADE, verbose_name='Раздел')
    question = models.TextField(verbose_name='Вопрос', unique=True)
    author = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Автор', **NULLABLE)

    def __str__(self):
        return f'{self.question}'

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ('id',)


class Answers(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, verbose_name='Вопрос')
    answer = models.CharField(max_length=255, verbose_name='Ответ')
    is_correct = models.BooleanField(default=False, verbose_name='Правильный ответ')
    not_correct = models.BooleanField(default=False, verbose_name='Неверный ответ')
    author = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Автор', **NULLABLE)

    def __str__(self):
        return f'{self.answer} - {self.is_correct}'

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
        ordering = ('id',)

    def save(self, *args, **kwargs):
        """Проверка ответа пользователя на уровне модели"""
        if self.not_correct is True and self.is_correct is True:
            raise ValidationError("Ответ может быть только верным или только неверным")
        elif self.not_correct is False and self.is_correct is False:
            raise ValidationError("Выбирите верный этот ответ или неверный")
        super().save(*args, **kwargs)
