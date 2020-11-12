from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'myapp'


urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('tasks/<int:task_id>/', views.TasksDetail.as_view(), name='task_detail'),
    path('tasks/', views.TasksView.as_view(), name='tasks'),
    path('completed/', views.TasksCompleted.as_view(), name='completed_tasks'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('complete_task/', views.CompleteNewTask.as_view(), name='complete_new_task'),
    path('admin_view/', views.AdministratorView.as_view(), name='admin_view'),
    path('tasks/delete/<int:task_id>/', views.DeleteTask.as_view(), name='delete_task'),
    path('adminusers/delete/<int:user_id>/', views.DeleteUser.as_view(), name='delete_user'),
    path('adminusers/addadmin/<int:user_id>/', views.MakeAdmin.as_view(), name='add_admin'),
    path('admintasks/', views.AdminTasks.as_view(), name='tasks_admin'),
    path('adminusers/<int:user_id>/', views.ViewUser.as_view(), name='specific_user'),
    path('adminusers/', views.AdminUsers.as_view(), name='admin_users'),
    path('', views.FirstPage.as_view(), name='first_page'),
]

if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



