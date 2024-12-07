from django.urls import path
from confirm_students.views import get_students, view_accommodation_pdf

app_name = 'confirm_students'

urlpatterns = [
    path("", get_students, name="get_students"),
    path("accommodation/<path:file_name>/", view_accommodation_pdf, name="view_accommodation_pdf"),
]