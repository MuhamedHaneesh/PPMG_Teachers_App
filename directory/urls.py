from django.urls import path
from . import views

urlpatterns = [
    path('', views.TeachersListView.as_view(), name='teachers_list'),
    path('import/', views.UploadFilesView.as_view(), name="import"),
    path('teacher/<int:pk>/', views.TeacherProfileView.as_view(), name='teacher_profile')
]
