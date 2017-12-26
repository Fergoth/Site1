from django.views.generic.list import ListView
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, HttpResponseRedirect
from .models import Course_Request,Request_offers,Approved_course,Transactions
from .forms import NewCourseForm,AcceptRequestForm,UploadFileForm
from django.shortcuts import render
from main.models import Profile
import os
from django.conf import settings
from django.http import HttpResponse




class CourseView(ListView):
    model = Course_Request
    template_name = r'course_work/templates/course.html'
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if context['object_list']:
            user = self.request.user
            if user.has_perm("main.customer"):
                qs = Course_Request.objects.all()
                context['object_list'] = context['object_list'].filter(owner_user=user.profile) #Если обычный пользователь показываем только его заказаные работы
            if user.has_perm("main.performer"):
                qs = Request_offers.objects.filter(owner_performer=user.profile)
                l=[]
                for q in qs:
                    l.append(q.course_request_id)
                if l:
                    context['Request_offers'] = l
        return context #Если исполнитель то возвращаем весь список
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perm("main.reviewer"):#Рецензенту нафиг не сдаля этот список
            return HttpResponseNotFound('<h1>No Page Here</h1>')
        return super(CourseView, self).dispatch(request, *args, **kwargs)


class NewCourseView(View):
    template_name = r'course_work/templates/new_course.html'
    
    def post(self,request,*args,**kwargs):
        form = NewCourseForm(request.POST,user=request.user)
        if form.is_valid():
            topic = form.cleaned_data['topic']
            if form.cleaned_data['university']:
                university = form.cleaned_data['university']
            else:
                university=''
            if form.cleaned_data['teacher']:
                teacher = form.cleaned_data['teacher']
            else:
                teacher=''
            min_price = form.cleaned_data['min_price']
            max_price = form.cleaned_data['max_price']
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
    template_name = r'course_work/templates/accept_request.html'
    
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

class DeleteRequestView(View):
    def post(self,request,*args,**kwargs):
        pk = kwargs.pop('pk')
        qs = Course_Request.objects.filter(pk=pk)
        if request.user.has_perm('main.customer') and qs[0].owner_user == request.user.profile:
            qs[0].delete()
            return HttpResponseRedirect('/course')
        #TODO Возвращать сообщение об ошибке
        return HttpResponseRedirect('/course')
    
class ChooseYourPerformerView(View):
    def post(self,request,*args,**kwargs):
        try:
            pk = kwargs.pop('pk')
        except KeyError:
            return HttpResponseRedirect('/course')
        #TODO Обработать ошибки
        try:
            performer = kwargs.pop('performer_id')
        except KeyError:
            return HttpResponseRedirect('/course')
        qs = Course_Request.objects.filter(pk=pk)
        qs2 = Request_offers.objects.filter(course_request_id=pk)
        qs2 = qs2.filter(owner_performer=performer)
        p=qs2[0].price
        t=qs[0].topic
        d=qs[0].description
        u=qs[0].university
        cust = qs[0].owner_user
        owner =qs2[0].owner_performer
        c = Approved_course(owner_user=cust,
                            owner_performer=owner,
                            price=p,
                            topic =t,
                            description=d,
                            university=u,
                            ready=False,
                            file='')
        
        cust =qs[0].owner_user
        qs3 =Profile.objects.get(pk = cust.pk)
        qs3.wallet.balance-=p
        if qs3.wallet.balance < 0 :
            pass
            #TODO обработать чтобы юзер не получал отрицательный счет :C
        t = Transactions(course=qs[0],from_profile=cust,to_profile=owner,sum=p)
        qs3.wallet.save()
        c.save()
        t.save()
        qs.delete()
        return HttpResponseRedirect('/course')
        
       
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perm('main.customer'):
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseNotFound('<h1>No Page Here</h1>')


class CompleteCourseView(ListView):
    model = Approved_course
    template_name = r'course_work/templates/approved_course.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if context['object_list']:
            user = self.request.user
            if user.has_perm("main.customer"):
                context['object_list'] = context['object_list'].filter(owner_user=user.profile)
            if user.has_perm("main.performer"):
                context['object_list']= context['object_list'].filter(owner_performer=user.profile)

        return context  # Если исполнитель то возвращаем весь список
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perm("main.reviewer"):  # Рецензенту нафиг не сдаля этот список
            return HttpResponseNotFound('<h1>No Page Here</h1>')
        return super(CompleteCourseView,self).dispatch(request, *args, **kwargs)

    
def upload_file(request, pk):
    if request.method == 'POST':
        a = Approved_course.objects.get(pk=pk)
        a.ready = True
        a.save()
        form = UploadFileForm(request.POST, request.FILES,instance=a)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/complete_course')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form,'pk':pk})


@login_required()
def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
       # a = Transactions.objects.get(course_id=pk)
      #  p=Profile.objects.get(pk = a.to_profile)
       # p.wallet.balance+=a.sum
       # p.wallet.save
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.pdf")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response


class RdyCourseView(ListView):
    model = Approved_course
    template_name = r'course_work/templates/rdy_course.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if context['object_list']:
            user = self.request.user
            if user.has_perm("main.customer"):
                context['object_list'] = context['object_list'].filter(
                    owner_user=user.profile)
            if user.has_perm("main.performer"):
                context['object_list'] = context['object_list'].filter(
                    owner_performer=user.profile)
        
        return context
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perm(
                "main.reviewer"):  # Рецензенту нафиг не сдаля этот список
            return HttpResponseNotFound('<h1>No Page Here</h1>')
        return super(RdyCourseView, self).dispatch(request, *args,
                                                        **kwargs)