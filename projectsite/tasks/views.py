from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.db.models import Count, Q
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from tasks.defaults import ensure_default_workspace_data
from tasks.models import Category, Task, Note, Priority, SubTask


class WorkspaceDefaultsMixin(LoginRequiredMixin):
    login_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        ensure_default_workspace_data()
        return super().dispatch(request, *args, **kwargs)


class HangarinLogoutView(LogoutView):
    next_page = reverse_lazy('login')
    http_method_names = ['get', 'post', 'head', 'options']

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


# Home/Dashboard View
class HomePageView(WorkspaceDefaultsMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = "home.html"

    def get_queryset(self):
        return Task.objects.select_related('category', 'priority').order_by('-updated_at')[:6]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = Task.objects.select_related('category', 'priority')
        task_count = tasks.count()
        pending_count = tasks.filter(status="Pending").count()
        in_progress_count = tasks.filter(status="In Progress").count()
        completed_count = tasks.filter(status="Completed").count()

        def build_status_row(label, count, tone):
            percent = round((count / task_count) * 100) if task_count else 0
            return {
                "label": label,
                "count": count,
                "percent": percent,
                "tone": tone,
            }

        context.update({
            'task_count': task_count,
            'category_count': Category.objects.count(),
            'priority_count': Priority.objects.count(),
            'subtask_count': SubTask.objects.count(),
            'note_count': Note.objects.count(),
            'pending_count': pending_count,
            'in_progress_count': in_progress_count,
            'completed_count': completed_count,
            'status_overview': [
                build_status_row("Pending", pending_count, "warning"),
                build_status_row("In Progress", in_progress_count, "info"),
                build_status_row("Completed", completed_count, "success"),
            ],
            'top_categories': Category.objects.annotate(task_total=Count('task')).order_by('-task_total', 'name')[:5],
            'recent_tasks': tasks.order_by('-updated_at')[:6],
            'upcoming_tasks': tasks.order_by('deadline')[:5],
            'today': timezone.localdate(),
        })
        return context


# Category Views
class CategoryList(WorkspaceDefaultsMixin, ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'category_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset


class CategoryCreateView(WorkspaceDefaultsMixin, CreateView):
    model = Category
    fields = ['name']
    template_name = 'category_form.html'
    success_url = reverse_lazy('category-list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['name'].widget.attrs.update({'class': 'form-control'})
        return form


class CategoryUpdateView(WorkspaceDefaultsMixin, UpdateView):
    model = Category
    fields = ['name']
    template_name = 'category_form.html'
    success_url = reverse_lazy('category-list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['name'].widget.attrs.update({'class': 'form-control'})
        return form


class CategoryDeleteView(WorkspaceDefaultsMixin, DeleteView):
    model = Category
    template_name = 'category_confirm_delete.html'
    success_url = reverse_lazy('category-list')


# Priority Views
class PriorityList(WorkspaceDefaultsMixin, ListView):
    model = Priority
    context_object_name = 'priorities'
    template_name = 'priority_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset.order_by('name')


class PriorityCreateView(WorkspaceDefaultsMixin, CreateView):
    model = Priority
    fields = ['name']
    template_name = 'priority_form.html'
    success_url = reverse_lazy('priority-list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['name'].widget.attrs.update({'class': 'form-control'})
        return form


class PriorityUpdateView(WorkspaceDefaultsMixin, UpdateView):
    model = Priority
    fields = ['name']
    template_name = 'priority_form.html'
    success_url = reverse_lazy('priority-list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['name'].widget.attrs.update({'class': 'form-control'})
        return form


class PriorityDeleteView(WorkspaceDefaultsMixin, DeleteView):
    model = Priority
    template_name = 'priority_confirm_delete.html'
    success_url = reverse_lazy('priority-list')


# Task Views
class TaskList(WorkspaceDefaultsMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'task_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().select_related('category', 'priority')
        query = self.request.GET.get('q')
        status = self.request.GET.get('status')
        priority = self.request.GET.get('priority')
        category = self.request.GET.get('category')

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )

        if status:
            queryset = queryset.filter(status=status)

        if priority:
            queryset = queryset.filter(priority_id=priority)

        if category:
            queryset = queryset.filter(category_id=category)

        return queryset.order_by('-deadline')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Task.STATUS_CHOICES
        context['priorities'] = Priority.objects.all()
        context['categories'] = Category.objects.all()
        return context


class TaskCreateView(WorkspaceDefaultsMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'deadline', 'status', 'priority', 'category']
    template_name = 'task_form.html'
    success_url = reverse_lazy('task-list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['title'].widget.attrs.update({'class': 'form-control'})
        form.fields['description'].widget.attrs.update({'class': 'form-control', 'rows': 4})
        form.fields['deadline'].widget.attrs.update({'class': 'form-control'})
        form.fields['status'].widget.attrs.update({'class': 'form-control'})
        form.fields['priority'].widget.attrs.update({'class': 'form-control'})
        form.fields['category'].widget.attrs.update({'class': 'form-control'})
        return form


class TaskUpdateView(WorkspaceDefaultsMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'deadline', 'status', 'priority', 'category']
    template_name = 'task_form.html'
    success_url = reverse_lazy('task-list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['title'].widget.attrs.update({'class': 'form-control'})
        form.fields['description'].widget.attrs.update({'class': 'form-control', 'rows': 4})
        form.fields['deadline'].widget.attrs.update({'class': 'form-control'})
        form.fields['status'].widget.attrs.update({'class': 'form-control'})
        form.fields['priority'].widget.attrs.update({'class': 'form-control'})
        form.fields['category'].widget.attrs.update({'class': 'form-control'})
        return form


class TaskDeleteView(WorkspaceDefaultsMixin, DeleteView):
    model = Task
    template_name = 'task_confirm_delete.html'
    success_url = reverse_lazy('task-list')


# SubTask Views
class SubTaskList(WorkspaceDefaultsMixin, ListView):
    model = SubTask
    context_object_name = 'subtasks'
    template_name = 'subtask_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().select_related('task')
        query = self.request.GET.get('q')
        status = self.request.GET.get('status')

        if query:
            queryset = queryset.filter(title__icontains=query)

        if status:
            queryset = queryset.filter(status=status)

        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = SubTask.STATUS_CHOICES
        return context


class SubTaskCreateView(WorkspaceDefaultsMixin, CreateView):
    model = SubTask
    fields = ['task', 'title', 'status']
    template_name = 'subtask_form.html'
    success_url = reverse_lazy('subtask-list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['task'].widget.attrs.update({'class': 'form-control'})
        form.fields['title'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter subtask title'})
        form.fields['status'].widget.attrs.update({'class': 'form-control'})
        return form


class SubTaskUpdateView(WorkspaceDefaultsMixin, UpdateView):
    model = SubTask
    fields = ['task', 'title', 'status']
    template_name = 'subtask_form.html'
    success_url = reverse_lazy('subtask-list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['task'].widget.attrs.update({'class': 'form-control'})
        form.fields['title'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter subtask title'})
        form.fields['status'].widget.attrs.update({'class': 'form-control'})
        return form


class SubTaskDeleteView(WorkspaceDefaultsMixin, DeleteView):
    model = SubTask
    template_name = 'subtask_confirm_delete.html'
    success_url = reverse_lazy('subtask-list')


# Note Views
class NoteList(WorkspaceDefaultsMixin, ListView):
    model = Note
    context_object_name = 'notes'
    template_name = 'note_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().select_related('task')
        query = self.request.GET.get('q')
        created = self.request.GET.get('created')
        if query:
            queryset = queryset.filter(content__icontains=query)
        if created:
            queryset = queryset.filter(created_at__date=created)
        return queryset.order_by('-created_at')


class NoteCreateView(WorkspaceDefaultsMixin, CreateView):
    model = Note
    fields = ['task', 'content']
    template_name = 'note_form.html'
    success_url = reverse_lazy('note-list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['task'].widget.attrs.update({'class': 'form-control'})
        form.fields['content'].widget.attrs.update({'class': 'form-control', 'rows': 4})
        return form


class NoteUpdateView(WorkspaceDefaultsMixin, UpdateView):
    model = Note
    fields = ['task', 'content']
    template_name = 'note_form.html'
    success_url = reverse_lazy('note-list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['task'].widget.attrs.update({'class': 'form-control'})
        form.fields['content'].widget.attrs.update({'class': 'form-control', 'rows': 4})
        return form


class NoteDeleteView(WorkspaceDefaultsMixin, DeleteView):
    model = Note
    template_name = 'note_confirm_delete.html'
    success_url = reverse_lazy('note-list')
