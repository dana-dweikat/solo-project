from django.views import View, generic
from django.db.models import Count
from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from jobboard.decorators import login_required
from .models import User, Job, Application
from .forms import UserRegistrationForm, LoginForm, ApplicationForm, JobForm


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        # Fetching data
        all_jobs = Job.objects.all()
        all_applications = Application.objects.all()
        all_users = User.objects.all()
        # Adding data to context
        context["jobs"] = all_jobs.annotate(application_count=Count("applications")).order_by("-application_count")[:5]
        context["jobs_count"] = all_jobs.count()
        context["application_count"] = all_applications.count()
        context["user_count"] = all_users.count()

        return context
    
class SignUpView(View):
    form_class = UserRegistrationForm
    template_name = 'login.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('app1:home')
        else:
            #display the first error
            error_message = next(iter(form.errors.values()))[0]
            messages.error(request, error_message)
            
        return redirect("app1:login_page")
    
#   render login page 
class LoginPageView(TemplateView):
    template_name = 'login.html'

    # for disappearing login button in login page :
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        # Adding data to context
        context["login_page"] = True
       
        return context

    #   for login button 
class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = 'login.html'
    
    def form_invalid(self, form):
        messages.error(self.request, "Invalid credentials.")
        return super().form_invalid(form)

    def get_success_url(self):
        next_url = self.request.session.get("next_path")
        if next_url:
            self.request.session["next_path"] = None
            return next_url
        return reverse_lazy("app1:home")
       

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("app1:login_page")
    
    

@method_decorator(login_required, name='dispatch')
class ViewAppliedJobDetails(generic.ListView):
    template_name = 'applied_jobs.html'
    context_object_name = 'applied_jobs'
   
# to filter only job the user applied for:
    def get_queryset(self):
        applications = self.request.user.applied_jobs.all()
        return Job.objects.filter(applications__in=applications)


@method_decorator(login_required, name='dispatch')
class ViewPostedJobDetails(generic.ListView):
    template_name = 'posted_jobs.html'
    context_object_name = 'posted_jobs'


 # to filter only job the user posted_jobs for:
    def get_queryset(self):
        return self.request.user.posted_jobs.all()

# browse job  list + job details
class BrowseJobView(View):  
    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")        
        return self.detail_view(request, pk) if pk else self.list_view(request)

    # to browse job details by job id:
    def detail_view(self, request, pk, *args, **kwargs):
        # by default the current user didn't applied , and not in the favorite.
        applied = is_favorite = False
        job = get_object_or_404(Job, pk=pk)
        if request.user.is_authenticated:
            applied = job.applications.filter(user=request.user).exists()
            is_favorite = request.user.favorite_jobs.filter(id=pk).exists()

        context = {"job": job, "applied": applied, "is_favorite": is_favorite}
        return render(request, "job-single.html", context)
    
    # to browse listed  job :
    def list_view(self, request, *args, **kwargs):
        all_jobs = Job.objects.all()
        context = {"jobs": all_jobs, "jobs_count": all_jobs.count()}
        return render(request, "job-listings.html", context)

# for create and edit posted job:
@method_decorator(login_required, name='dispatch')
class JobCreateEditView(generic.CreateView, generic.UpdateView):
    model = Job
    form_class = JobForm
    template_name = 'post-job.html'
    success_url = reverse_lazy('app1:posted_jobs')

# send context data to the template:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # for disappearing +post job button in post job form page : 
        context["post_job_page"] = True
        return context
    
    
    # to check if there an object(job) or not :
    def get_object(self, queryset=None):
        if self.kwargs.get('pk'):  # If pk is present, it's an edit request
            return get_object_or_404(Job, pk=self.kwargs['pk'])
        else:  # Otherwise, it's a create request
            return None
    
  # if edit or none:
    def get_template_names(self):
        if self.object:  # If self.object is exist, it's an edit request so  render  edit html
            return ["edit-job.html"]
        else:  # Otherwise, it's a create request  so render (post job form -html)
            return [self.template_name]
    
    
    def form_invalid(self, form):
        error_message = next(iter(form.errors.values()))[0]
        messages.error(self.request, error_message)
        return super().form_invalid(form)
    
    # if valid  assign current user as job creator (posted job)
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')    
class DeleteJobView(View):
    def get(self, request, pk, *args, **kwargs):    
        Job.objects.filter(id=pk).delete()
        return redirect("app1:posted_jobs")


@method_decorator(login_required, name='dispatch')
class JobApplicationView(generic.edit.CreateView):
    model = Application
    form_class = ApplicationForm
    template_name = 'apply.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job'] = get_object_or_404(Job, id=self.kwargs['pk'])
        return context

    def form_invalid(self, form):
        error_message = next(iter(form.errors.values()))[0]
        messages.error(self.request, error_message)
        return super().form_invalid(form)
    
    def form_valid(self, form):
        form.instance.job = get_object_or_404(Job, id=self.kwargs['pk'])
        form.instance.user = self.request.user
        return super().form_valid(form)
# if   form is valid: function is success go to this url:
    def get_success_url(self):
        return reverse_lazy('app1:applied_jobs')
    
  # delete user job application 
@method_decorator(login_required, name='dispatch')
class DeleteAppliedJob(View):
    def get(self, request, *args, **kwargs):    
        job = Job.objects.get(id=kwargs["pk"])
        job.applications.filter(user=request.user).delete()
        return redirect("app1:applied_jobs")



@method_decorator(login_required, name='dispatch')
class AddFavoriteJobView(View):
    def get(self, request, *args, **kwargs):
        job = get_object_or_404(Job, id=kwargs["pk"])
        request.user.favorite_jobs.add(job)
        return redirect(reverse("app1:job_details", kwargs={"pk": kwargs["pk"]}))
    
        
@method_decorator(login_required, name='dispatch')
class FavoritePageView(generic.ListView):
    template_name = 'favorite.html'
    context_object_name = 'favorite_jobs'

# filter  favorite jobs that user has

    def get_queryset(self):
        return self.request.user.favorite_jobs.all()


@method_decorator(login_required, name='dispatch')
class RemoveFavoriteJobView(View):            
    def get(self, request, *args, **kwargs):
        job = get_object_or_404(Job, id=kwargs["pk"])
        self.request.user.favorite_jobs.remove(job)
        return redirect(reverse("app1:job_details", kwargs={"pk": kwargs["pk"]}))
