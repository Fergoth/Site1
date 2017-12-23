from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from .models import Course_Request


class CourseView(ListView):
    model = Course_Request
    template_name = r'course_work\templates\course.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if context['object_list']:
            user = self.request.user
            context['object_list'] = context['object_list'].filter(owner_user=user.profile)
        return context
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CourseView, self).dispatch(request, *args, **kwargs)

class NewCourseView(TemplateView):
    template_name = r'course_work\templates\new_course.html'
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perm('main.customer'):
            return super(NewCourseView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseNotFound('<h1>No Page Here</h1>')