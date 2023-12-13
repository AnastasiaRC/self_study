from django.urls import path
from study.apps import StudyConfig
from study.views import MaterialsListAPIView, MaterialsDetailAPIView, MaterialsUpdateAPIView, MaterialsCreateAPIView, \
    MaterialsDeleteAPIView, QuestionsCreateAPIView, AnswersCreateAPIView, QuestionsDeleteAPIView, AnswersDeleteAPIView, \
    QuestionsUpdateAPIView, AnswersUpdateAPIView, TopicsDeleteAPIView, TopicsUpdateAPIView, TopicsCreateAPIView, \
    TopicsDetailAPIView, TopicsListAPIView, QuestionsListAPIView, AnswersListAPIView

app_name = StudyConfig.name

urlpatterns = [
    path('topics/', TopicsListAPIView.as_view(), name='topics_list'),
    path('topics/<int:pk>/', TopicsDetailAPIView.as_view(), name='topics_detail'),
    path('topics/create/', TopicsCreateAPIView.as_view(), name='topics_create'),
    path('topics/update/<int:pk>/', TopicsUpdateAPIView.as_view(), name='topics_update'),
    path('topics/delete/<int:pk>/', TopicsDeleteAPIView.as_view(), name='topics_delete'),

    path('materials/', MaterialsListAPIView.as_view(), name='materials_list'),
    path('materials/<int:pk>/', MaterialsDetailAPIView.as_view(), name='materials_detail'),
    path('materials/create/', MaterialsCreateAPIView.as_view(), name='materials_create'),
    path('materials/update/<int:pk>/', MaterialsUpdateAPIView.as_view(), name='materials_update'),
    path('materials/delete/<int:pk>/', MaterialsDeleteAPIView.as_view(), name='materials_delete'),

    path('questions/', QuestionsListAPIView.as_view(), name='list_questions'),
    path('questions/create/', QuestionsCreateAPIView.as_view(), name='create_questions'),
    path('questions/update/<int:pk>/', QuestionsUpdateAPIView.as_view(), name='update_questions'),
    path('questions/delete/<int:pk>/', QuestionsDeleteAPIView.as_view(), name='delete_questions'),

    path('answers/', AnswersListAPIView.as_view(), name='list_answers'),
    path('answers/create/', AnswersCreateAPIView.as_view(), name='create_answers'),
    path('answers/update/<int:pk>/', AnswersUpdateAPIView.as_view(), name='update_answers'),
    path('answers/delete/<int:pk>/', AnswersDeleteAPIView.as_view(), name='delete_answers'),
]
