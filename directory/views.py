from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Teacher, Subject
from django.views.generic.detail import DetailView


# Create your views here.
class UploadFilesView(ListView):
    pass


class TeachersListView(ListView):
    model = Teacher
    template_name = 'contact/teachers_list.html'

    def get_queryset(self):
        queryset = self.model.objects.all()
        if self.request.GET.get('val'):
            val = self.request.GET.get('val')
            if self.request.GET.get('type') and self.request.GET.get('type') == 'name':
                queryset = queryset.filter(last_name__istartswith=val)
            if self.request.GET.get('type') and self.request.GET.get('type') == 'subject':
                queryset = queryset.filter(subjects__name__istartswith=val)
        return queryset


class TeacherProfileView(DetailView):
    pass
