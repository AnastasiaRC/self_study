from django.contrib import admin
from study.models import Materials, Questions, Answers, Topics


@admin.register(Topics)
class TopicsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'author',)
    list_filter = ('author',)
    search_fields = ('description', 'title',)
    list_display_links = ('title',)


@admin.register(Materials)
class MaterialsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'study_topic',)
    list_filter = ('author',)
    search_fields = ('description',)
    list_display_links = ('title',)


@admin.register(Questions)
class QestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'author', 'item_materials',)
    list_filter = ('author',)
    search_fields = ('question', 'author',)
    list_display_links = ('question',)


@admin.register(Answers)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'answer', 'is_correct', 'author', 'question',)
    list_filter = ('author',)
    search_fields = ('answer', 'author',)
    list_display_links = ('answer',)
