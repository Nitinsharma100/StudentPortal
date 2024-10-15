from django.urls import path
from .import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.home,name='home'),
    path('notes',views.notes,name='notes'),
    path('delete_note<int:pk>/',views.delete_note,name='deletenote'),
    path('notes_detail<int:pk>/',views.NotesDetailView.as_view(),name='notedetail'),
    path('home_work/',views.homework,name='homework'),
    path('update_homework/<int:pk>',views.update_homework,name='updatehomework'),
    path('delete_homework/<int:pk>',views.delete_homework,name='deletehomework'),
    path('youtube/',views.youtube,name='youtube'),
    path('todo/',views.todo,name='todo'),
    path('delete_todo/<int:pk>',views.delete_todo,name='deletetodo'),
    path('books/',views.books,name='books'),
    path('dictionary/',views.dictionary,name='dictionary'),
    path('wiki/',views.wiki,name='wiki'),
    path('conversion/',views.conversion,name='conversion'),
    path('register/',views.register,name='register'),
    path('login/',auth_views.LoginView.as_view(template_name='dashboard/login.html'),name='login'),
    path('profile/',views.profile,name='profile'),

    path('logout/', auth_views.LogoutView.as_view(template_name='dashboard/logout.html'), name='logout'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('updatetodo/<int:pk>',views.updatetodo,name='updatetodo'),
    
    
]
