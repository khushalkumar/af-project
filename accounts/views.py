from django.shortcuts import render, redirect
from .models import CustomUser, CustomUserManager
from datetime import datetime, date
# Create your views here.
def form(request):
    if request.method == 'POST':
        pwd = request.POST['password1']
        if (len(pwd) < 6):
            return render(request, 'accounts/user-form.html', {'error': 'password must be atleast 6 digits long.'})

        if not any(char.isdigit() for char in pwd):
            return render(request, 'accounts/user-form.html', {'error': "password must have atleast 1 digit."})

        if not any(char.isalpha() for char in pwd):
            return render(request, 'accounts/user-form.html', {'error': "password must have atleast 1 letter."})

        if not any(char.isupper() for char in pwd):
            return render(request, 'accounts/user-form.html', {'error': "password must have atleast 1 upper case letter."})

        if(request.POST['date'] == ''):
            return render(request, 'accounts/user-form.html', {'error': "Date of Birth is required."})

        ph = request.POST['phonenumber']
        if not(ph.startswith('7') or ph.startswith('8') or ph.startswith('9')):
            return render(request, 'accounts/user-form.html', {'error': "Phone number should start with 7 or 8 or 9."})

        if(len(ph) > 10):
            return render(request, 'accounts/user-form.html', {'error': "Phone number should only have 10 digits."})

        if((request.POST['firstname'] == '') or (request.POST['lastname']) or (request.POST['phonenumber'])):
              return render(request, 'accounts/user-form.html', {'error': "All fields are required."})

        if ((request.POST['password1'] != '') or (request.POST['password2'] != '')):
            if (request.POST['password1'] == request.POST['password2']):
                datetoday_temp = str(datetime.date(datetime.now()))
                datetoday = datetoday_temp.split('-')
                born_temp = str(request.POST['date'])
                born = born_temp.split('-')

                # if request.POST['dob']  == (datetime.date(datetime.now())):
                # born = request.POST['date']
                # today = (datetime.date(datetime.now()))
                age = int(datetoday[0]) - int(born[0]) - ((int(datetoday[1]), int(datetoday[2])) < (int(born[1]), int(born[2])))
                if born > datetoday:
                    return render(request, 'accounts/user-form.html', {'error': 'Date should not be a future date.'})
                else:
                    if age < 18:
                        return render(request, 'accounts/user-form.html', {'error': 'Age is less than 18.'})
                    else:
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
                return render(request, 'accounts/user-form.html', {'error': 'Passwords do not match.'})
        else:
            return render(request, 'accounts/user-form.html', {'error': "Password can't be empty."})
    else:
        return render(request, 'accounts/user-form.html')


def thankyou(request):
    return render(request, 'accounts/thankyou.html')


def home(request):
    return render(request, 'accounts/home.html')
