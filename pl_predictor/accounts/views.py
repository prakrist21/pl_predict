from django.shortcuts import render, redirect
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm

User = get_user_model()

def RegisterView(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            verify_url = request.build_absolute_uri(
                f'/accounts/verify/{uid}/{token}/'
            )
            html = render_to_string('accounts/verification_email.html', {
                'verify_url': verify_url,
                'username': user.username,
            })
            msg = EmailMultiAlternatives(
                'Verify your email',
                f'Click the link to verify your account:\n\n{verify_url}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
            )
            msg.attach_alternative(html, 'text/html')
            msg.send()
            return redirect('verification_sent')
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (ValueError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.is_verified = True
        user.save()
        return redirect('login')

    return render(request, 'accounts/verification_failed.html')


def verification_sent(request):
    return render(request, 'accounts/verification_sent.html')