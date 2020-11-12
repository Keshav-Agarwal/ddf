from django.shortcuts import render
from django.views import View
from .forms import TasksForm, SignupForm, LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Tasks, CompletedTasks
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Sum
from django.contrib.auth.models import Permission
from django.contrib.auth.mixins import UserPassesTestMixin




# Create your views here.
# sum = 


class TasksView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        tasks = Tasks.objects.all()
        for t in tasks:
            if(len(CompletedTasks.objects.filter(user__pk=request.user.id, task__pk=t.pk)) > 0):
                t.done = True
            else:
                t.done = False
        print("skfhbsjhdfbs", tasks)
        return render(request, 'myapp/tasks.html', {'tasks':tasks})



class TasksCompleted(LoginRequiredMixin, View):
    
    def get(self, request, *args, **kwargs):
        current_user_id = request.user.id
        completed_tasks = CompletedTasks.objects.filter(user=current_user_id)
        return render(request, 'myapp/completed_tasks.html', {'completed_tasks':completed_tasks})


class ProfileView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        current_user_id = request.user.id
        user = User.objects.get(pk=current_user_id)
        points = CompletedTasks.objects.filter(user__pk=current_user_id).aggregate(Sum('task__points'))
        return render(request, 'myapp/profile.html', {'user':user, 'points':points })


class TasksDetail(LoginRequiredMixin, View):
    
    def get(self, request, *args, **kwargs):
        task_id = kwargs['task_id']
        task = Tasks.objects.get(pk=task_id)
        
        return render(request, 'myapp/task_detail.html', {'task':task})


class CompleteNewTask(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        completed_task = CompletedTasks()
        task_id = request.POST['task_id']
        proof_ss = request.FILES['proof_ss']
        completed_task.user = request.user
        completed_task.task = Tasks.objects.get(pk=task_id) 
        completed_task.completed_task_ss = proof_ss
        completed_task.save()
        return redirect("myapp:completed_tasks")



#-------ADMIN--------------


class AdministratorView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('myapp.add_tasks', 'myapp.delete_tasks', 'myapp.edit_tasks', )


    def get(self, request, *args, **kwargs):
        return render(request, 'myapp/app_admin.html')        


    def post(self, request, *args, **kwargs):
        task_ss = request.FILES['task_logo']
        task_name = request.POST['task_name']
        task_url = request.POST['task_url']
        category = request.POST['category']
        points = request.POST['points']

        task = Tasks()
        task.task_ss = task_ss    
        task.task_name = task_name
        task.task_url = task_url
        task.category = category
        task.points = points
        task.save()


        return render(request, 'myapp/app_admin.html')



class DeleteTask(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('myapp.add_tasks', 'myapp.delete_tasks', 'myapp.edit_tasks', )

    def get(self, request, *args, **kwargs):
        task_id = kwargs['task_id']
        Tasks.objects.filter(pk=task_id).delete()
        return redirect("myapp:tasks_admin")




class AdminTasks(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('myapp.add_tasks', 'myapp.delete_tasks', 'myapp.edit_tasks', )

    def get(self, request, *args, **kwargs):
        tasks = Tasks.objects.all()
        return render(request, 'myapp/tasks_admin.html', {'tasks':tasks})



class AdminUsers(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('myapp.add_tasks', 'myapp.delete_tasks', 'myapp.edit_tasks', )

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        return render(request, 'myapp/users_admin.html', {'users':users})



class ViewUser(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('myapp.add_tasks', 'myapp.delete_tasks', 'myapp.edit_tasks', )

    def get(self, request, *args, **kwargs):
        user_id = kwargs['user_id']
        user = User.objects.get(pk=user_id)
        completed_tasks = CompletedTasks.objects.filter(user=user)
        return render(request, 'myapp/view_user.html', {'user':user, 'completed_tasks':completed_tasks})



class DeleteUser(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('myapp.add_tasks', 'myapp.delete_tasks', 'myapp.edit_tasks', 'auth.add_user')

    def get(self, request, *args, **kwargs):
        user_id = kwargs['user_id']
        User.objects.get(pk=user_id).delete()
        return redirect("myapp:admin_users")
       


class MakeAdmin(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('auth.add_user')
    
    def get(self, request, *args, **kwargs):
        user_id = kwargs['user_id']

        permission1 = Permission.objects.get(codename='add_tasks')
        permission2 = Permission.objects.get(codename='delete_tasks')
        permission3 = Permission.objects.get(codename='edit_tasks')

        User.objects.get(pk=user_id).user_permissions.add(permission1, permission2, permission3)

        return redirect("myapp:admin_users")





# USER REGISTRATION AND AUTHENTICATION


class FirstPage(View):
    def get(self, request, *args, **kwargs):
        if(not request.user.is_authenticated):
            login_form = LoginForm()
            signup_form = SignupForm()
            return render(request, 'myapp/first_page.html', {
                'login_form':login_form,
                'signup_form':signup_form
            })
        else:
            return redirect("myapp:tasks")


class RegisterView(View):

    def post(self, request, *args, **kwargs):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("myapp:tasks")
        messages.error(request, "Something went wrong, please try again.")
        return redirect("myapp:first_page")


class LoginView(View):
    
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("myapp:tasks")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
        return redirect("myapp:first_page")



def logout_view(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("myapp:first_page")