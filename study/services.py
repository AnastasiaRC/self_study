from study.models import Questions, Answers, Topics, Materials


def testing():

    count_true = 0
    count_false = 0

    topics = Topics.objects.all().values_list('id', 'title', flat=False)
    for id_topics, title_topic in topics:
        print(f'{id_topics}. {title_topic}')
    id_topic = input("Выбирите номер темы:\n")

    materials = Materials.objects.filter(study_topic=id_topic).values_list('id', 'title', flat=False)
    for id_materials, title_materials in materials:
        print(f'{id_materials}. {title_materials}')
    id_material = input("Выбирите номер раздела:\n")

    questions = Questions.objects.filter(item_materials=id_material).values_list('id', 'question', flat=False)
    for id_questions, title_question in questions:
        print(f'{id_questions}. {title_question}')
        answers = Answers.objects.filter(question=id_questions).values_list('id', 'answer', 'is_correct', flat=False)
        while True:
            num_answer = 1
            for id_answer, answer, is_correct_answer in answers:
                print(f'   {num_answer}. {answer}')
                num_answer += 1
            user_answer = input("Введите номер ответа:\n")

            try:
                if answers[int(user_answer) - 1][2] is True:
                    print("Верно!")
                    count_true += 1
                else:
                    print("Неверно!")
                    count_false += 1
            except IndexError:
                print('Введите номер ответа из предложеных')
                num_answer = 0
                continue
            break
    print(
        f"Статистика, из {count_true + count_false} вопросов:\nПравельных ответов: {count_true}\nНеправильных ответов: {count_false}")
