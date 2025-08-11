from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth 

# Create your views here.

def register(request): 
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already exists")
                return render(request, "register.html")
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email already exists")
                return render(request, "register.html")
            else:
                user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
                user.save() 
                print("User created successfully") 
                return redirect("login")
        else:
            messages.info(request, "Passwords do not match")
            return render(request, "register.html")

    else:
        return render(request, "register.html")
 
def login(request):
    if request.method == "POST":
        username_or_email = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        username = None

        if "@" in username_or_email:
            try:
                user_obj = User.objects.get(email__iexact=username_or_email) 
                username = user_obj.username
            except User.DoesNotExist:
                messages.info(request, "Invalid credentials")
                return render(request, "login.html")
        else:
            username = username_or_email

        # Authenticate only if a username is present
        if username:
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect("home")
        
        messages.info(request, "Invalid credentials")
        return render(request, "login.html")
    else:
        return render(request, "login.html")  
    
def logout(request):
    auth.logout(request)
    return redirect('login')  # Redirect to login page after logout