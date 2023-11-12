from typing import Any
from django.db import connection
from django.shortcuts import render,redirect
from django.http import HttpRequest, HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import task

class userlogin(LoginView):
    template_name='base/login.html'
    redirect_authenticated_user= True

    def get_success_url(self) -> str:
        return reverse_lazy('tasks') 


class useregister(FormView):
    template_name='base/register.html'
    form_class= UserCreationForm
    success_url=reverse_lazy('tasks')

    def form_valid(self,form):
        #user=form.save()
        #FLAW 5 A02:2021-Cryptographic Failures
        #START
        user = form.save(commit=False)
        plaintext_password = form.cleaned_data['password1'] 
        user.password = plaintext_password
        user.save()
        user.backend = 'base.password_backend.passwordbackend'
        #CONTINUATION IN settings.py+password_backend.py
        if user is not None:
            login(self.request,user)
        return super(useregister,self).form_valid(form)
    

    def get(self,*args, **kwargs) :
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(useregister,self).get(*args, **kwargs) 

class tasklist(LoginRequiredMixin,ListView):
    model= task
    context_object_name='tasks'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        #FLAW 1 A01:2021:Broken Access Control
        #context['tasks']= context['tasks'].filter(user=self.request.user) 
        context['count']= context['tasks'].filter(complete=False).count() 

        search_input=self.request.GET.get('search-area') or ''
        ''' if search_input:
                context['tasks']=context['tasks'].filter(title__icontains=search_input)'''
        #FLAW 2:A03:2021:Injection
        #START
        if search_input:
            with connection.cursor() as cursor:
                query = "SELECT * FROM base_task WHERE title LIKE '%%%s%%'" % search_input
                cursor.execute(query)
                rows = cursor.fetchall()
            context['tasks'] = [self.model(id=row[0], user_id=row[1], title=row[2], description=row[3], complete=row[4], time=row[5]) for row in rows]
        else:
            context['tasks'] = self.model.objects.all()
        #END
        context['search_input']= search_input
        return context

class taskdetail(LoginRequiredMixin,DetailView):
    model= task
    context_object_name='task'

class taskcreate(LoginRequiredMixin,CreateView):
    model = task
    fields=['title','description','complete']
    success_url=reverse_lazy('tasks') 
    def form_valid(self,form):
        form.instance.user=self.request.user
        return super(taskcreate,self).form_valid(form)
    
class taskupdate(LoginRequiredMixin,UpdateView):
    model=task
    fields=['title','description','complete']
    success_url=reverse_lazy('tasks')

class taskdelete(LoginRequiredMixin,DeleteView):
    model=task
    context_object_name='task'
    fields='__all__'
    template_name = 'base/task_delete.html'
    success_url=reverse_lazy('tasks')
