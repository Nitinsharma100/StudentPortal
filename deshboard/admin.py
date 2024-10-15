from django.contrib import admin
from .models import Notes,Homework,Todo
# Register your models here.
@admin.register(Notes)
class NotesAdminModel(admin.ModelAdmin):
    list_display=['id','user','title','description']
@admin.register(Homework)
class NotesAdminModel(admin.ModelAdmin):
    list_display=['id','user','subject','title','description','due','is_finished']
    
@admin.register(Todo)
class NotesAdminModel(admin.ModelAdmin):
    list_display=['id','user','title','desc','is_finished']
    
