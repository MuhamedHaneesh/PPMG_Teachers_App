from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Teacher, Subject
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateResponseMixin, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Teacher, Subject
from .forms import UploadFileForm
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os, shutil
import csv
from io import TextIOWrapper
from zipfile import ZipFile
from django.contrib import messages
from django.core.files import File


# Create your views here.
class UploadFilesView(LoginRequiredMixin, TemplateResponseMixin, View):
    template_name = 'directory/import.html'

    def get(self, request, *args, **kwargs):
        form = UploadFileForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        upload_path = settings.STYLES_ROOT.joinpath('images/teachers').joinpath('teachers.zip')
        if os.path.exists(upload_path):
            os.remove(upload_path)
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            self.handle_uploaded_file(request.FILES['images'], upload_path)
            self.read_csv_file(request.FILES['names'].file, upload_path, request, form)
        return render(request, self.template_name, {'form': form})

    def handle_uploaded_file(self, image_file, upload_path):
        with open(upload_path, 'wb+') as destination:
            for chunk in image_file.chunks():
                destination.write(chunk)

    def read_csv_file(self, csv_file, upload_path, request, form):
        csv_data_in_bytes = TextIOWrapper(csv_file,
                                          encoding='utf-8')
        csv_data = csv.DictReader(csv_data_in_bytes)
        archived_images = ZipFile(upload_path, 'r')
        try:
            for row in csv_data:
                if row['First Name'].strip() == '' or row['Email Address'].strip() == '':
                    raise Exception('First Name / Email cant be blank')
                teacher = Teacher()
                teacher.first_name = row['First Name'].strip()
                teacher.last_name = row['Last Name'].strip()
                teacher.email = row['Email Address'].strip()
                teacher.phone = row['Phone Number'].strip()
                teacher.room_no = row['Room Number'].strip()
                teacher.save()
                subjects = row['Subjects taught'].split(',')
                if row['Profile picture'] in archived_images.namelist():
                    image = archived_images.open(row['Profile picture'], 'r')
                    df = File(image)
                    teacher.profile_picture.save(row['Profile picture'], df, save=True)
                for subj in subjects:
                    if subj != '':
                        subject, _ = Subject.objects.get_or_create(name=subj.strip().upper())
                        if teacher.subjects.count() < 5:
                            teacher.subjects.add(subject)
            messages.success(request, 'Data saved successfully')
        except Exception as e:
            messages.info(request, e)
        finally:
            archived_images.close();


class TeachersListView(ListView):
    model = Teacher
    template_name = 'directory/teachers_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['last_name_chars'] = self.get_the_last_name_chars()
        context['subject_chars'] = self.get_the_last_subject_chars()
        return context

    def get_the_last_name_chars(self):
        last_name_chars = []
        for row in Teacher.objects.values_list('last_name', flat=True).filter(
                last_name__isnull=False).exclude(last_name='').order_by('last_name').distinct():
            first_char = row.strip().upper()[0]
            if first_char not in last_name_chars:
                last_name_chars.append(first_char)
        return last_name_chars

    def get_the_last_subject_chars(self):
        subject_chars = []
        for row in Subject.objects.values_list('name', flat=True).filter(
                name__isnull=False).exclude(name='').order_by('name').distinct():
            first_char = row.strip().upper()[0]
            if first_char not in subject_chars:
                subject_chars.append(first_char)
        return subject_chars

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
    model = Teacher
