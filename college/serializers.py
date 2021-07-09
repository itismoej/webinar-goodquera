from rest_framework import serializers

from college.models import College, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CollegeSerializer(serializers.ModelSerializer):
    lesson_set = LessonSerializer(many=True)

    class Meta:
        model = College
        fields = ('id', 'name', 'lesson_set',)
