"""
URL configuration for projectsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from allauth.account.views import LoginView
from tasks.views import (
    HomePageView,
    HangarinLogoutView,
    CategoryList,
    CategoryCreateView,
    CategoryUpdateView,
    CategoryDeleteView,
    PriorityList,
    PriorityCreateView,
    PriorityUpdateView,
    PriorityDeleteView,
    TaskList,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    NoteList,
    NoteCreateView,
    NoteUpdateView,
    NoteDeleteView,
    SubTaskList,
    SubTaskCreateView,
    SubTaskUpdateView,
    SubTaskDeleteView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('login/', LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', HangarinLogoutView.as_view(), name='logout'),
    path('', HomePageView.as_view(), name='home'),

    path('categories/', CategoryList.as_view(), name='category-list'),
    path('categories/new/', CategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),

    path('priorities/', PriorityList.as_view(), name='priority-list'),
    path('priorities/new/', PriorityCreateView.as_view(), name='priority-create'),
    path('priorities/<int:pk>/edit/', PriorityUpdateView.as_view(), name='priority-update'),
    path('priorities/<int:pk>/delete/', PriorityDeleteView.as_view(), name='priority-delete'),

    path('tasks/', TaskList.as_view(), name='task-list'),
    path('tasks/new/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/<int:pk>/edit/', TaskUpdateView.as_view(), name='task-update'),
    path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),

    path('notes/', NoteList.as_view(), name='note-list'),
    path('notes/new/', NoteCreateView.as_view(), name='note-create'),
    path('notes/<int:pk>/edit/', NoteUpdateView.as_view(), name='note-update'),
    path('notes/<int:pk>/delete/', NoteDeleteView.as_view(), name='note-delete'),

    path('subtasks/', SubTaskList.as_view(), name='subtask-list'),
    path('subtasks/new/', SubTaskCreateView.as_view(), name='subtask-create'),
    path('subtasks/<int:pk>/edit/', SubTaskUpdateView.as_view(), name='subtask-update'),
    path('subtasks/<int:pk>/delete/', SubTaskDeleteView.as_view(), name='subtask-delete'),
]
