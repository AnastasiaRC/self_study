from rest_framework import serializers
from study.models import Materials, Questions, Answers, Topics


class TopicsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topics
        fields = '__all__'


class MaterialsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Materials
        fields = '__all__'


class QuestionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Questions
        fields = '__all__'


class AnswersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answers
        fields = '__all__'
