from rest_framework import status
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from college.base_views import APIView
from college.models import College, Lesson
from college.permissions import IsCollegeMember
from college.serializers import CollegeSerializer, LessonSerializer
from core.api_utils import get_object_or_404


class LessonDetailView(APIView):
    permission_classes = {
        "get": [IsAdminUser | IsCollegeMember],
        "put": [IsAdminUser]
    }

    def get(self, request: Request, *args, lesson_id: int, **kwargs) -> Response:
        lesson: Lesson = get_object_or_404(Lesson, id=lesson_id)
        serialized_lesson = LessonSerializer(instance=lesson)
        return Response(serialized_lesson.data, status=status.HTTP_200_OK)

    def put(self, request: Request, *args, lesson_id: int, **kwargs) -> Response:
        lesson: Lesson = get_object_or_404(Lesson, id=lesson_id)
        serialized_lesson = CollegeSerializer(instance=lesson, data=request.data)
        if serialized_lesson.is_valid():
            serialized_lesson.save()
            return Response(serialized_lesson.data, status=status.HTTP_200_OK)
        return Response(serialized_lesson.errors, status=status.HTTP_400_BAD_REQUEST)


class LessonsView(APIView):
    permission_classes = {
        "get": [IsAdminUser | IsCollegeMember],
        "post": [IsAdminUser]
    }

    def get(self, request: Request, *args, college_id: int, **kwargs) -> Response:
        lessons = Lesson.objects.filter(college__id=college_id)
        serialized_lessons = LessonSerializer(instance=lessons, many=True)
        return Response(serialized_lessons.data)

    def post(self, request: Request, *args, **kwargs) -> Response:
        serialized_lessons = LessonSerializer(data=request.data)
        if serialized_lessons.is_valid():
            serialized_lessons.save()
            return Response(serialized_lessons.data, status=status.HTTP_201_CREATED)
        return Response(serialized_lessons.errors, status=status.HTTP_400_BAD_REQUEST)


class CollegeDetailView(APIView):
    permission_classes = {
        "get": [IsAdminUser | IsCollegeMember],
        "put": [IsAdminUser]
    }

    def get(self, request: Request, college_id: int, *args, **kwargs) -> Response:
        college: College = get_object_or_404(College, id=college_id)
        serialized_college = CollegeSerializer(instance=college)
        return Response(serialized_college.data, status=status.HTTP_200_OK)

    def put(self, request: Request, *args, college_id: int, **kwargs) -> Response:
        college: College = get_object_or_404(College, id=college_id)
        serialized_college = CollegeSerializer(instance=college, data=request.data)
        if serialized_college.is_valid():
            serialized_college.save()
            return Response(serialized_college.data, status=status.HTTP_200_OK)
        return Response(serialized_college.errors, status=status.HTTP_400_BAD_REQUEST)


class CollegesView(APIView):
    permission_classes = {
        "get": [IsAuthenticated],
        "post": [IsAdminUser]
    }

    def get(self, request: Request, *args, **kwargs) -> Response:
        if request.user.is_superuser:
            colleges = College.objects.all()
        else:
            colleges = request.user.college_set.all()

        serialized_colleges = CollegeSerializer(instance=colleges, many=True)
        return Response(serialized_colleges.data)

    def post(self, request: Request, *args, **kwargs) -> Response:
        serialized_college = CollegeSerializer(data=request.data)
        if serialized_college.is_valid():
            serialized_college.save()
            return Response(serialized_college.data, status=status.HTTP_201_CREATED)
        return Response(serialized_college.errors, status=status.HTTP_400_BAD_REQUEST)


class CollegeRegister(APIView):
    permission_classes = {
        "get": [~IsCollegeMember],
    }

    def get(self, request: Request, *args, college_id: int, **kwargs) -> Response:
        college: College = get_object_or_404(College, id=college_id)
        msg, success = college.add_member(request.user)
        status_code = status.HTTP_200_OK if success else status.HTTP_400_BAD_REQUEST
        return Response({'detail': msg}, status=status_code)
