from django.urls import path

from . import views

app_name = "app1"


urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("login-page/", views.LoginPageView.as_view(), name="login_page"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("view-job-list/", views.BrowseJobView.as_view(), name="list_jobs"),
    path("view-job-details/<int:pk>/", views.BrowseJobView.as_view(), name="job_details"),
    path('post-job/', views.JobCreateEditView.as_view(), name='post_edit_job'),
    path('post-job/<int:pk>/', views.JobCreateEditView.as_view(), name='post_edit_job'),
    path("delete-job/<int:pk>/", views.DeleteJobView.as_view(), name="delete_job"),
    path("applied-jobs/", views.ViewAppliedJobDetails.as_view(), name="applied_jobs"),
    path("posted-jobs/", views.ViewPostedJobDetails.as_view(), name="posted_jobs"),
    path("apply/<int:pk>/", views.JobApplicationView.as_view(), name="apply"),
    path(
        "delete-application/<int:pk>/",
        views.DeleteAppliedJob.as_view(),
        name="delete_application",
    ),
    path('favorite/<int:pk>/', views.AddFavoriteJobView.as_view(), name='favorite'),
    path('remove_favorite/<int:pk>/', views.RemoveFavoriteJobView.as_view(), name='remove_favorite'),
    path('favorite_page/', views.FavoritePageView.as_view(), name='favorite_page')    
]
