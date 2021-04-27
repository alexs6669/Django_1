from django.conf import settings
from django.contrib import auth
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm, ShopUserProfileEditForm
from authapp.models import ShopUser


def login(request):
    title = 'вход'
    login_form = ShopUserLoginForm(data=request.POST or None)
    next = request.GET.get('next', '')
    # next = request.GET['next'] if 'next' in request.GET else ''

    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponseRedirect(reverse('main'))

    content = {
        'title': title,
        'login_form': login_form,
        'next': next
    }
    return render(request, 'authapp/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))


def send_verify_email(user):
    verify_link = reverse('auth:verify', args=[user.username, user.activation_key])
    subject = f'Подтверждение учетной записи {user.username} на портале {settings.DOMAIN_NAME}'
    message = f'Ссылка для активации учетной записи: {settings.DOMAIN_NAME}{verify_link}'
    from_addr = settings.EMAIL_HOST_USER
    to_addr = user.email
    my_pass = settings.EMAIL_HOST_PASSWORD
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    server = smtplib.SMTP('smtp.yandex.ru:465')
    server.starttls()
    server.login(from_addr, my_pass)
    server.sendmail(from_addr, to_addr, msg.as_string())
    ret = server.quit()
    if ret == '-1':
        return False
    else:
        return True

    # return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=True)


def verify(request, activation_key):
    user = ShopUser.objects.get(activation_key=activation_key)
    if user.activation_key == activation_key and not user.is_activation_key_expired():
        user.is_active = True
        user.activation_key = ''
        user.save()
        auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')

    return render(request, 'authapp/verification.html')


def register(request):
    title = 'регистрация'

    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            user = register_form.save()
            if send_verify_email(user):
                print('Verification email sent successfully')
            else:
                print('Failed to sent verification email')

            return HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = ShopUserRegisterForm()

    content = {
        'title': title,
        'form': register_form
    }
    return render(request, 'authapp/register.html', content)


def edit(request):
    title = 'редактирование'

    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        profile_form = ShopUserProfileEditForm(request.POST, instance=request.user.shopuserprofile)
        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))

    else:
        edit_form = ShopUserEditForm(instance=request.user)
        profile_form = ShopUserProfileEditForm(instance=request.user.shopuserprofile)

    content = {
        'title': title,
        'edit_form': edit_form,
        'profile_form': profile_form
    }

    return render(request, 'authapp/edit.html', content)
