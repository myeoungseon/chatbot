from django.contrib import admin
from django.urls import path, reverse
from django.shortcuts import redirect
from django import forms
from django.template.response import TemplateResponse
 
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from .utils import *
from .models import *

class ChatHistoryAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'query', 'answer')
    list_filter = ('datetime',)
    search_fields = ('query', 'answer')

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField()
 
class VectorAdmin(admin.ModelAdmin):
    list_display = ('category', 'content')
    actions = ['delete']
   
    add_form_template = 'admin/vector/change_form.html'
 
    def delete(self, request, queryset):
        queryset.delete()
        reset_chunk_db()
        self.message_user(request, "Chroma DB has been reset and selected objects have been deleted.")
    delete.short_description = "Delete selected objects and reset Chroma DB"
   
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload-csv/', self.admin_site.admin_view(self.upload_csv), name='vector_upload_csv'),
        ]
        return custom_urls + urls
 
    def upload_csv(self, request):
        if request.method == 'POST':
            form = CSVUploadForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = request.FILES['csv_file']
                csv_to_sqlite(csv_file)
                self.message_user(request, "CSV file uploaded successfully")
                reset_chunk_db()
                return redirect('..')
        else:
            form = CSVUploadForm()
 
        context = {
            'form': form,
            'title': 'Upload CSV',
            'app_label': self.model._meta.app_label,
        }
        return TemplateResponse(request, 'admin/vector/upload_csv.html', context)
   
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
   
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        reset_chunk_db()  
   
    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['upload_csv_url'] = reverse('admin:vector_upload_csv')
        extra_context['app_label'] = self.model._meta.app_label
        return super().add_view(request, form_url=form_url, extra_context=extra_context)

admin.site.register(Vector, VectorAdmin)
admin.site.register(ChatHistory, ChatHistoryAdmin)

