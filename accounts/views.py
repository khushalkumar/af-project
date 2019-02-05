from django.shortcuts import render, redirect
from .models import CustomUser, CustomUserManager

# Create your views here.
def form(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = CustomUser.objects.get(email = request.POST['email'])
                return render(request, 'accounts/user-form.html', {'error': 'email ID already exists'})
            except CustomUser.DoesNotExist:
                #
                # dateofbirth = request.POST['dob']
                # dateofbirth2 = dateofbirth.split('-')
                # d = ['1','2','3']
                # d[0] = dateofbirth2[2]
                # d[1] = dateofbirth2[1]
                # d[2] = dateofbirth2[0]
                # d = str(d)
                user = CustomUser.objects.create_user(email=request.POST['email'], password= request.POST['password1'], first_name= request.POST['firstname'], last_name= request.POST['lastname'], dob= request.POST['date'], phone_number= request.POST['phonenumber'])
                # auth.login(request, user)
                return redirect('thankyou')
        else:
            return render(request, 'accounts/user-form.html', {'error': 'passwords do not match'})
    else:
        return render(request, 'accounts/user-form.html')


def thankyou(request):
    return render(request, 'accounts/thankyou.html')


def home(request):
    return render(request, 'accounts/home.html')
