from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from study.models import Materials, Topics, Questions, Answers
from users.models import User


class MaterialsTestCase(APITestCase):
    def setUp(self):
        self.maxDiff = None
        self.user = User.objects.create(
            email="test@yandex.by",
            first_name="test",
            last_name="test",
            is_superuser=False,
            is_staff=False,
            is_active=True,
        )
        self.user.set_password("1234")
        self.user.save()

        token = RefreshToken.for_user(self.user)
        self.access_token = str(token.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

        self.topic = Topics.objects.create(
            title='Маркетинг',
            description="Реклама и продажи",
            author=self.user
        )

        self.topic2 = Topics.objects.create(
            title="Дизайн",
            description="Фотошоп копирайтинг",
            author=self.user
        )

        self.materials = Materials.objects.create(
            title="Реклама",
            description="Упаковка билборды",
            study_topic=self.topic,
            author=self.user,
        )

        self.materials2 = Materials.objects.create(
            title="Грфический дизайн",
            description="Приложения сайты",
            study_topic=self.topic,
            author=self.user,
        )

        self.question = Questions.objects.create(
            question="Что такое реклама?",
            item_materials=self.materials,
            author=self.user,
        )

        self.question2 = Questions.objects.create(
            question="Что такое дизайн?",
            item_materials=self.materials,
            author=self.user,
        )

        self.answer = Answers.objects.create(
            question=self.question,
            answer="Она повышает узнаваемость",
            is_correct=True,
            not_correct=False,
            author=self.user,
        )

        self.answer2 = Answers.objects.create(
            question=self.question,
            answer="Она не взаимодействует с интернетом",
            is_correct=False,
            not_correct=True,
            author=self.user,
        )

    def test_topics_list(self):
        """ Тест получения списка тем """
        response = self.client.get(reverse("study:topics_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {"count": 2,
                          "next": None,
                          "previous": None,
                          "results": [
                              {
                                  "id": self.topic.id,
                                  "title": self.topic.title,
                                  "description": self.topic.description,
                                  "author": self.topic.author.id
                              },
                              {
                                  "id": self.topic2.id,
                                  "title": self.topic2.title,
                                  "description": self.topic2.description,
                                  "author": self.topic2.author.id
                              }]})

    def test_topics_list_view_pk(self):
        """ Тест получения отдельной темы """
        response = self.client.get(reverse("study:topics_detail", args=(self.topic2.pk,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {"id": self.topic2.id,
                          "title": self.topic2.title,
                          "description": self.topic2.description,
                          "author": self.topic2.author.id})

    def test_topics_create(self):
        """Тест создания тем"""
        data = {"title": "Физика",
                "description": "Функции и задачи", }

        response = self.client.post(reverse("study:topics_create"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(3, Topics.objects.all().count())
        self.assertTrue(Topics.objects.all().exists())

    def test_topics_create_error(self):
        """Тест создание тем с ошибкой валидации"""
        data = {"title": "физика",
                "description": "Функции и задачи", }

        response = self.client.post(reverse("study:topics_create"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(2, Topics.objects.all().count())
        self.assertTrue(Topics.objects.all().exists())

    def test_topics_update(self):
        """ Тест обновления тем """
        data = {"id": self.topic.pk,
                "title": "Биология",
                "description": self.topic.description, }

        response = self.client.put(reverse("study:topics_update", args=(self.topic.pk,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.topic.refresh_from_db()
        self.assertEqual(self.topic.title, data["title"])

    def test_topics_delete(self):
        """ Тест удаления темы """

        response = self.client.delete(reverse("study:topics_delete", args=(self.topic.pk,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(1, Topics.objects.all().count())

    def test_materials_list(self):
        """ Тест получения списка разделов """
        response = self.client.get(reverse("study:materials_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {"count": 2,
                          "next": None,
                          "previous": None,
                          "results": [
                              {"id": self.materials.id,
                               "title": self.materials.title,
                               "description": self.materials.description,
                               "study_topic": self.materials.study_topic.id,
                               "author": self.materials.author.id},
                              {"id": self.materials2.id,
                               "title": self.materials2.title,
                               "description": self.materials2.description,
                               "study_topic": self.materials2.study_topic.id,
                               "author": self.materials2.author.id}
                          ]})

    def test_materials_list_view_pk(self):
        """ Тест получения отдельного раздела """
        response = self.client.get(reverse("study:materials_detail", args=(self.materials.pk,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {"id": self.materials.id,
                          "title": self.materials.title,
                          "description": self.materials.description,
                          "study_topic": self.materials.study_topic.id,
                          "author": self.materials.author.id})

    def test_materials_create(self):
        """Тест создания раздела"""
        data = {"title": "Задачи",
                "description": "Что требуется выполнить",
                "study_topic": self.materials.study_topic.id, }

        response = self.client.post(reverse("study:materials_create"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(3, Materials.objects.all().count())
        self.assertTrue(Materials.objects.all().exists())

    def test_materials_create_error(self):
        """Тест создание раздела с ошибкой валидации"""
        data = {"title": "задачи",
                "description": "Что требуется выполнить", }

        response = self.client.post(reverse("study:materials_create"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(2, Materials.objects.all().count())
        self.assertTrue(Materials.objects.all().exists())

    def test_materials_update(self):
        """ Тест обновления раздела """
        data = {"id": self.materials.pk,
                "title": "Цели",
                "description": self.materials.description,
                "study_topic": self.materials.study_topic.id}

        response = self.client.put(reverse("study:materials_update", args=(self.materials.pk,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.materials.refresh_from_db()
        self.assertEqual(self.materials.title, data["title"])

    def test_materials_delete(self):
        """ Тест удаления раздела """

        response = self.client.delete(reverse("study:materials_delete", args=(self.materials.pk,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(1, Materials.objects.all().count())

    def test_questions_list(self):
        """ Тест получения списка вопросов """
        response = self.client.get(reverse("study:list_questions"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         [{"id": self.question.id,
                           "item_materials": self.question.item_materials.id,
                           "question": self.question.question,
                           "author": self.question.author.id},
                          {"id": self.question2.id,
                           "item_materials": self.question.item_materials.id,
                           "question": self.question2.question,
                           "author": self.question2.author.id}])

    def test_questions_create(self):
        """Тест создания вопроса"""
        data = {"item_materials": self.question.item_materials.id,
                "question": "Что такое маркетинг?", }

        response = self.client.post(reverse("study:create_questions"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(3, Questions.objects.all().count())
        self.assertTrue(Questions.objects.all().exists())

    def test_questions_update(self):
        """ Тест обновление вопроса """
        data = {"id": self.question.pk,
                "question": "Что такое биология?",
                "item_materials": self.question.item_materials.id, }

        response = self.client.put(reverse("study:update_questions", args=(self.question.pk,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.question.refresh_from_db()
        self.assertEqual(self.question.question, data["question"])

    def test_questions_delete(self):
        """ Тест удаление вопроса """

        response = self.client.delete(reverse("study:delete_questions", args=(self.question.pk,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(1, Questions.objects.all().count())

    def test_answers_list(self):
        """ Тест получения списка ответов """
        response = self.client.get(reverse("study:list_answers"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         [{"id": self.answer.id,
                           "question": self.answer.question.id,
                           "answer": self.answer.answer,
                           "is_correct": self.answer.is_correct,
                           "not_correct": self.answer.not_correct,
                           "author": self.answer.author.id},

                          {"id": self.answer2.id,
                           "question": self.answer2.question.id,
                           "answer": self.answer2.answer,
                           "is_correct": self.answer2.is_correct,
                           "not_correct": self.answer2.not_correct,
                           "author": self.answer2.author.id}
                          ])

    def test_answers_create(self):
        """Тест создания ответа"""
        data = {"question": self.answer2.question.id,
                "answer": "Это наука",
                "is_correct": True,
                "not_correct": False, }

        response = self.client.post(reverse("study:create_answers"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(3, Answers.objects.all().count())
        self.assertTrue(Answers.objects.all().exists())

    def test_answers_create_error(self):
        """Тест создания ответа с ошибкой на валидацию"""
        data = {"question": self.answer.question.id,
                "answer": "Это наука",
                "is_correct": False,
                "not_correct": False, }

        response = self.client.post(reverse("study:create_answers"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(2, Answers.objects.all().count())
        self.assertTrue(Answers.objects.all().exists())

    def test_answers_create_error_2(self):
        """Тест создания ответа с ошибкой на валидацию"""
        data = {"question": self.answer2.question.id,
                "answer": "Это наука",
                "is_correct": True,
                "not_correct": True, }

        response = self.client.post(reverse("study:create_answers"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(2, Answers.objects.all().count())
        self.assertTrue(Answers.objects.all().exists())

    def test_answers_update(self):
        """ Тест обновление ответа """
        data = {"id": self.answer.id,
                "question": self.answer.question.id,
                "answer": "Это наука изучающая природу",
                "is_correct": self.answer.is_correct,
                "not_correct": self.answer.not_correct, }

        response = self.client.put(reverse("study:update_answers", args=(self.answer.pk,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.answer.refresh_from_db()
        self.assertEqual(self.answer.answer, data["answer"])

    def test_answers_delete(self):
        """ Тест удаление ответа """

        response = self.client.delete(reverse("study:delete_answers", args=(self.answer.pk,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(1, Answers.objects.all().count())

    def tearDown(self) -> None:
        self.user.delete()
        self.topic.delete()
        self.topic2.delete()
        self.materials.delete()
        self.materials2.delete()
        self.question.delete()
        self.question2.delete()
        self.answer.delete()
        self.answer2.delete()
