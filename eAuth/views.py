from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate



# Authenticataion Part
class RegisterationView(View):
    
    def get(self, request):
        return render(request, 'eAuth/signup.html')
    
    
    
    def post(self, request):
        
        if request.method == "POST":
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password = request.POST['password']
            c_psd = request.POST['c_psd']
            
            if password != c_psd:
                messages.warning(request, 'Password is not Matching.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
            user = User.objects.create_user(username=email, email=email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            
            messages.success(request, 'Your Account has been Succesfully Created. Please Login In')
            return redirect('signin')
            
            
        return render(request, 'eAuth/signup.html')
    
    
    
    

def signin(request):
    
    if not request.user.is_authenticated:
    
        if request.method == "POST":
            email = request.POST['email']
            password = request.POST['password']
            
            
            user = authenticate(username=email, password=password)
            
            if user is not None:
                login(request, user)
                # messages.success(request, 'Login Succes')
                return redirect('home')
            
            messages.error(request, 'Invaild Credentails.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    else:
        return redirect('home')
        
    return render(request, 'eAuth/signin.html')



    
    
class SignoutView(View):
    
    def get(self, request):
        logout(request)
        messages.info(request, 'Logout Success.')
        return redirect('signin')