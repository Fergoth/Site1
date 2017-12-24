from django.views.generic.list import ListView
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, HttpResponseRedirect
from .models import Course_Request,Request_offers
from .forms import NewCourseForm,AcceptRequestForm
from django.shortcuts import render



class CourseView(ListView):
    model = Course_Request
    template_name = r'course_work\templates\course.html'
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if context['object_list']:
            user = self.request.user
            if user.has_perm("main.customer"):
                context['object_list'] = context['object_list'].filter(owner_user=user.profile) #Если обычный пользователь показываем только его заказаные работы
        return context #Если исполнитель то возвращаем весь список
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perm("main.reviewer"):#Рецензенту нафиг не сдаля этот список
            return HttpResponseNotFound('<h1>No Page Here</h1>')
        return super(CourseView, self).dispatch(request, *args, **kwargs)


class NewCourseView(View):
    template_name = r'course_work\templates\new_course.html'
    
    def post(self,request,*args,**kwargs):
        form = NewCourseForm(request.POST,user=request.user)
        if form.is_valid():
            topic = form.cleaned_data['topic']
            if form.cleaned_data['university']:
                university = form.cleaned_data['university']
            if form.cleaned_data['teacher']:
                teacher = form.cleaned_data['teacher']
            min_price= form.cleaned_data['min_price']
            max_price = form.cleaned_data['min_price']
            description = form.cleaned_data['description']
            c = Course_Request(
                owner_user=request.user.profile,
                topic=topic,
                description=description,
                university=university,
                teacher=teacher,
                min_price=min_price,
                max_price=max_price
            )
            c.save()
            return HttpResponseRedirect('/course')
        return render(request, self.template_name, {'form': form})
    
    def get(self,request,*args,**kwargs):
        form = NewCourseForm()
        return render(request, self.template_name, {'form': form})
            
            
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perm('main.customer'):
            return super(NewCourseView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseNotFound('<h1>No Page Here</h1>')


class AcceptRequestView(View):
    template_name = r'course_work\templates\accept_request.html'
    
    def post(self, request, *args, **kwargs):
        pk = kwargs.pop('pk')
        qs = Course_Request.objects.filter(pk=pk)
        form = AcceptRequestForm(request.POST,qs=qs)
        if form.is_valid():
            price = form.cleaned_data['price']
            c = Request_offers(course_request=qs[0], price=int(price),owner_performer=request.user.profile)
            c.save()
            return HttpResponseRedirect('/course')
        return render(request, self.template_name, {'form': form,'qs': qs})

    def get(self,request,*args,**kwargs):
        pk = kwargs.pop('pk')
        qs = Course_Request.objects.filter(pk=pk)
        form = AcceptRequestForm()
        return render(request, self.template_name, {'form': form, 'qs': qs} )
    