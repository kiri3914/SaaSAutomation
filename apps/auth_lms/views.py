from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apps.users.models import CustomUser
from apps.students.models import Student
from apps.mainapp.models import Mentor


class FindUserView(APIView):
    models_map = {
        "student": Student,
        "mentor": Mentor,
        "branch_manager": CustomUser,
    }

    @swagger_auto_schema(
        operation_description="Поиск пользователя по email среди студентов, менторов и менеджеров",
        manual_parameters=[
            openapi.Parameter(
                "email",
                openapi.IN_QUERY,
                description="Email пользователя для поиска",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description="Информация о пользователе",
                examples={
                    "application/json": {
                        "id": 12,
                        "full_name": "Иван Иванов",
                        "email": "test@mail.com",
                        "phone": "+77001234567",
                        "role": "student",
                        "branch": "Алматы",
                        "course": "Python Backend",
                    }
                },
            ),
            400: "Email is required",
            404: "User not found",
        },
    )
    def get(self, request):
        email = request.GET.get("email")
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        user_data = self._find_user_by_email(email)
        if not user_data:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(user_data, status=status.HTTP_200_OK)

    def _find_user_by_email(self, email: str):
        for role, model in self.models_map.items():
            obj = model.objects.filter(email=email).first()
            if obj:
                return {
                    "id": obj.id,
                    "full_name": getattr(obj, "full_name", f"{getattr(obj, 'first_name', '')} {getattr(obj, 'last_name', '')}".strip()),
                    "email": obj.email,
                    "phone": getattr(obj, "phone", None),
                    "role": role,
                    "branch": getattr(obj, "branch_id", None), 
                    "course": getattr(obj, "course_id", None)
                }
        return None
