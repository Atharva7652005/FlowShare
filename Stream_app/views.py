from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import re
import os
from .models import StorageEntry, StorageFiles
from .forms import RegisterForm

# Admin authentication check
def is_admin(user):
    return user.is_authenticated and user.username == 'admin'

# Admin login view
def admin_login(request):
    error = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username == "admin" and password == "Khairnar@2005":
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('admin_dashboard')
            else:
                error = "Admin user not found. Please create admin user in Django admin."
        else:
            error = "Invalid admin credentials."
    return render(request, "login.html", {"error": error})

# Admin dashboard view
@user_passes_test(is_admin, login_url='/admin_login')
def admin_dashboard(request):
    from django.contrib.auth.models import User
    total_users = User.objects.count()
    total_rooms = StorageEntry.objects.count()
    users = User.objects.all()
    rooms = StorageEntry.objects.all()
    return render(request, "admin_dashboard.html", {
        "total_users": total_users,
        "total_rooms": total_rooms,
        "users": users,
        "rooms": rooms
    })

# Delete user (admin only)
@user_passes_test(is_admin, login_url='/admin_login')
def admin_delete_user(request, user_id):
    if request.method == "POST":
        user = get_object_or_404(User, id=user_id)
        # Delete user's storage rooms and files
        user_rooms = StorageEntry.objects.filter(storage_code=user.username)
        for room in user_rooms:
            admin_delete_room_helper(room)
        user.delete()
        return redirect('admin_dashboard')
    return HttpResponseBadRequest("Invalid request")

# Delete storage room (admin only)
@user_passes_test(is_admin, login_url='/admin_login')
def admin_delete_room(request, room_id):
    if request.method == "POST":
        room = get_object_or_404(StorageEntry, id=room_id)
        admin_delete_room_helper(room)
        return redirect('admin_dashboard')
    return HttpResponseBadRequest("Invalid request")

# Helper to delete room and files
def admin_delete_room_helper(room):
    files = StorageFiles.objects.filter(storage_entry_id=room)
    for f in files:
        # Delete file from storage
        if f.storage_files:
            file_path = f.storage_files.path
            if os.path.exists(file_path):
                os.remove(file_path)
        f.delete()
    room.delete()

# Home view
def home(request): 
    return render(request, 'home.html')

def streamify_info(request):
    return render(request, 'streamify_info.html')


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
    app_id = os.environ.get('APP_ID', 0)
    server_secret = os.environ.get('SERVER_SECRET', '')
    return render(request, 'videoCall.html', {
        'name': request.user.username,
        'app_id': app_id,
        'server_secret': server_secret
    })

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
    return render(request, "drop_file.html")


def get_file(request):
    return render(request, "get_file.html")

@csrf_exempt
def api_upload(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("Only POST allowed")

    storage_id = request.POST.get('storage_id', '').strip()
    if not re.fullmatch(r'\d{4}', storage_id):
        return JsonResponse({'error': 'storage_id must be a 4-digit string'}, status=400)

    files = request.FILES.getlist('files')
    if not files:
        return JsonResponse({'error': 'No files uploaded'}, status=400)

    # Prevent collision: if a StorageEntry already exists with this storage_code, reject.
    if StorageEntry.objects.filter(storage_code=storage_id).exists():
        return JsonResponse({'error': 'Storage ID already exists'}, status=409)

    entry = StorageEntry.objects.create(storage_code=storage_id)
    created_files = []
    for f in files:
        sf = StorageFiles.objects.create(storage_entry_id=entry, storage_files=f)
        created_files.append({
            'filename': sf.storage_files.name.split('/')[-1],
            'size': sf.storage_files.size,
            'url': request.build_absolute_uri(sf.storage_files.url)
        })

    return JsonResponse({
        'success': True,
        'storage_id': storage_id,
        'files': created_files,
        'message': f'Uploaded {len(created_files)} file(s)'
    }, status=201)


def api_get_files(request, storage_id):
    if not re.fullmatch(r'\d{4}', storage_id):
        return JsonResponse({'error': 'invalid storage id'}, status=400)
    try:
        entry = StorageEntry.objects.get(storage_code=storage_id)
    except StorageEntry.DoesNotExist:
        return JsonResponse({'error': 'not found'}, status=404)

    files = []
    for sf in entry.storage_files.all():
        try:
            size = sf.storage_files.size
        except (FileNotFoundError, OSError):
            size = 0  # or None, indicating file is missing locally
            
        files.append({
            'filename': sf.storage_files.name.split('/')[-1],
            'size': size,
            'download_url': request.build_absolute_uri(sf.storage_files.url)
        })
    return JsonResponse({'storage_id': storage_id, 'files': files})
