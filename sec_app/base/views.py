from typing import Any
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
# Create your views here.
'''
HNAYA USER FLAW CAN BE HAD HIT LA L USER ACCCEDA LINK W ANA HAY
HADI HE WILL BE ABLE TO ACCESS STUFF MACHI DIALO hadik import loginrequiredmixin
page it oveerides the not logged in user to is in setting.py
also users can access other users stuff so you add getcontext_data to prevent them
'''
 

class userlogin(LoginView):
    template_name='base/login.html'
    #fields='__all__'
    redirect_authenticated_user= True

    def get_success_url(self) -> str:
        return reverse_lazy('tasks') #difference between this and otehrs is makaynch f attrib i guess-->


class useregister(FormView):
    template_name='base/register.html'
    form_class= UserCreationForm
    success_url=reverse_lazy('tasks')
    def form_valid(self,form):
        user=form.save()
        if user is not None:
            login(self.request,user)
        return super(useregister,self).form_valid(form)
    def get(self,*args, **kwargs) :
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(useregister,self).get(*args, **kwargs) #redirects to main page if u try to register when ure already logged in

class tasklist(LoginRequiredMixin,ListView):
    model= task
    #if u dont have ur html thg i taybda b the first name hna it will giev u an error que makaynch a correspoonding template
    context_object_name='tasks' #to change dik objectlist f html temp
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['tasks']= context['tasks'].filter(user=self.request.user) #make sure that only teh user can acces it
        context['count']= context['tasks'].filter(complete=False).count() #get count of incomplete items

        search_input=self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks']=context['tasks'].filter(title__icontains=search_input) #search change icontains to startwith if u want more to search by what it starts with
        context['search_input']= search_input
        return context

class taskdetail(LoginRequiredMixin,DetailView):
    model= task
    context_object_name='task'
    #you can change template name by using template_name = 'base/x.html'

class taskcreate(LoginRequiredMixin,CreateView):
    model = task
    #by default this view had a model form
    fields=['title','description','complete']#stops it from listing all users
    success_url=reverse_lazy('tasks') #when an item is created user is sent back to the list
    '''to limit creation to only teh user logeed in instead of having user choose cah ydir'''
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

