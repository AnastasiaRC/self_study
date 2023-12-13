from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, \
    ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from study.models import Materials, Questions, Answers, Topics
from study.paginators import Pagination
from study.serializers import MaterialsSerializer, TopicsSerializer, QuestionsSerializer, AnswersSerializer
from study.permissions import IsAuthor, IsAdmin


class TopicsCreateAPIView(CreateAPIView):
    """Создание темы"""
    serializer_class = TopicsSerializer
    queryset = Topics.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_topic = serializer.save()
        new_topic.author = self.request.user
        new_topic.save()


class TopicsListAPIView(ListAPIView):
    """Отображение всех тем"""
    serializer_class = TopicsSerializer
    queryset = Topics.objects.all()
    pagination_class = Pagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('title', 'description',)
    permission_classes = [IsAuthenticated]


class TopicsDetailAPIView(RetrieveAPIView):
    """Отображение отдельной темы"""
    serializer_class = TopicsSerializer
    queryset = Topics.objects.all()
    permission_classes = [IsAuthenticated]


class TopicsUpdateAPIView(UpdateAPIView):
    """Обновление темы"""
    serializer_class = TopicsSerializer
    queryset = Topics.objects.all()
    permission_classes = [IsAuthor | IsAdmin]


class TopicsDeleteAPIView(DestroyAPIView):
    """Удаление темы"""
    serializer_class = TopicsSerializer
    queryset = Topics.objects.all()
    permission_classes = [IsAdmin | IsAuthor]


class MaterialsListAPIView(ListAPIView):
    """Отображение всех разделов"""
    serializer_class = MaterialsSerializer
    queryset = Materials.objects.all()
    pagination_class = Pagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('title', 'description',)
    ordering_fields = ('study_topic',)
    permission_classes = [IsAuthenticated]


class MaterialsDetailAPIView(RetrieveAPIView):
    """Отображение отдельного раздела"""
    serializer_class = MaterialsSerializer
    queryset = Materials.objects.all()
    permission_classes = [IsAuthenticated]


class MaterialsCreateAPIView(CreateAPIView):
    """Создание раздела"""
    serializer_class = MaterialsSerializer
    queryset = Materials.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_material = serializer.save()
        new_material.author = self.request.user
        new_material.save()


class MaterialsUpdateAPIView(UpdateAPIView):
    """Обновление раздела"""
    serializer_class = MaterialsSerializer
    queryset = Materials.objects.all()
    permission_classes = [IsAuthor | IsAdmin]


class MaterialsDeleteAPIView(DestroyAPIView):
    """Удаление раздела"""
    serializer_class = MaterialsSerializer
    queryset = Materials.objects.all()
    permission_classes = [IsAuthor | IsAdmin]


class QuestionsListAPIView(ListAPIView):
    """Отображение всех вопросов"""
    queryset = Questions.objects.all()
    serializer_class = QuestionsSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('question',)
    ordering_fields = ('item_materials',)
    permission_classes = [IsAuthenticated]


class QuestionsCreateAPIView(CreateAPIView):
    """Создание вопроса"""
    queryset = Questions.objects.all()
    serializer_class = QuestionsSerializer
    permission_classes = [IsAdmin | IsAuthor]

    def perform_create(self, serializer):
        new_question = serializer.save()
        new_question.author = self.request.user
        new_question.save()


class QuestionsUpdateAPIView(UpdateAPIView):
    """Обновление вопроса"""
    queryset = Questions.objects.all()
    serializer_class = QuestionsSerializer
    permission_classes = [IsAdmin | IsAuthor]


class QuestionsDeleteAPIView(DestroyAPIView):
    """Удаление вопроса"""
    queryset = Questions.objects.all()
    serializer_class = QuestionsSerializer
    permission_classes = [IsAdmin | IsAuthor]


class AnswersListAPIView(ListAPIView):
    """Просмотр всех ответов"""
    queryset = Answers.objects.all()
    serializer_class = AnswersSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('answer',)
    ordering_fields = ('question',)
    permission_classes = [IsAuthenticated]


class AnswersCreateAPIView(ListCreateAPIView):
    """Создание ответа"""
    queryset = Answers.objects.all()
    serializer_class = AnswersSerializer
    permission_classes = [IsAdmin | IsAuthor]

    def perform_create(self, serializer):
        new_answer = serializer.save()
        new_answer.author = self.request.user
        new_answer.save()


class AnswersUpdateAPIView(UpdateAPIView):
    """Обновление ответа"""
    queryset = Answers.objects.all()
    serializer_class = AnswersSerializer
    permission_classes = [IsAdmin | IsAuthor]


class AnswersDeleteAPIView(DestroyAPIView):
    """Удаление ответа"""
    queryset = Answers.objects.all()
    serializer_class = AnswersSerializer
    permission_classes = [IsAdmin | IsAuthor]
