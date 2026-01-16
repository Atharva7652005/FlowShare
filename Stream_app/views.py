from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm

# Home view
def home(request): 
    return render(request, 'home.html')


# Register view
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

        # show errors only after submit
        return render(request, "register.html", {
            "form": form,
            "submitted": True
        })

    # First render (GET request)
    form = RegisterForm()
    return render(request, "register.html", {
        "form": form,
        "submitted": False
    })


# Login view
def login(request):
    error = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')
        else:
            error = "Invalid username or password"

    return render(request, "login.html", {
        "error": error
    })

@login_required(login_url='/login')
def dashboard(request):
    return render(request, "dashboard.html")

@login_required(login_url='/login')
def videocall(request):
    return render(request, 'videoCall.html', {'name': request.user.username})

@login_required(login_url='/login')
def join_meeting(request):
    if request.method == 'POST':
        roomID = request.POST['roomID']
        return redirect("/meeting?roomID="+roomID)
    
    return render(request, 'join_room.html', {'name': request.user.username})

def logout_streamify(request):
    print("logout successully")
    logout(request)
    request.session.flush()
    return redirect("/login")

def drop_file(request):
    print("Drop File")


def get_file(request):
    print("Get File")