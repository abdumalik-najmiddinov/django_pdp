import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model
from django.contrib.auth import login, authenticate, logout
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, ListView

from app.models import Course, Teacher, Blog
from bot_tg import send_telegram_message
import asyncio


class IndexView(TemplateView):
    template_name = 'index.html'


class AboutView(TemplateView):
    template_name = 'about.html'


class VerifView(TemplateView):
    template_name = 'verify_code.html'


class ClassesView(TemplateView):
    template_name = 'class.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.all()
        return context


class TeachersView(ListView):
    template_name = 'team.html'
    paginate_by = 4
    context_object_name = "teachers"
    model = Teacher

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['range'] = range(1, 6)
        context["search_query"] = self.request.GET.get("q", "")
        return context

    def get_queryset(self):
        queryset = Teacher.objects.all()
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q)
            )
        return queryset


class GalleryView(TemplateView):
    template_name = 'gallery.html'


class BlogView(TemplateView):
    template_name = 'blog.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blogs'] = Blog.objects.all()
        return context


class BlogDetailView(TemplateView):
    template_name = 'single.html'


class ContactView(TemplateView):
    template_name = 'contact.html'

    def post(self, request, *args, **kwargs):
        name = request.POST.get("your_name")
        email = request.POST.get("gmail")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        telegram_text = f"""
Yangi Contact xabar!
Ism: {name}
Email: {email}
Subject: {subject}
Message: {message}
"""

        try:
            # Async funksiyani to'g'ri chaqirish
            asyncio.run(send_telegram_message(telegram_text))
            success = "Xabaringiz yuborildi!"
        except Exception as e:
            print("Telegram xabar yuborishda xato:", e)
            success = "Xabar yuborishda xatolik yuz berdi."

        return render(request, "contact.html", {"success": success})
def send_verification_email(to_email, code):
    sender_email = ""
    sender_password = ""

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = "Your Verification Code"

    body = f"Your verification code is: {code}"
    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, message.as_string())


User = get_user_model()


class AuthView(View):
    template_name = "auth.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("home")
        return render(request, self.template_name)

    def post(self, request):

        if "register_submit" in request.POST:
            email = request.POST.get("email")
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")

            if password1 != password2:
                return render(request, self.template_name, {"error": "Parollar mos emas"})

            if User.objects.filter(email=email).exists():
                return render(request, self.template_name, {"error": "Email mavjud"})

            code = random.randint(100000, 999999)

            request.session["verification_code"] = str(code)
            request.session["pending_user"] = {
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "password": password1,
            }

            send_verification_email(email, code)

            return redirect("verify")

        if "verify_code_submit" in request.POST:
            input_code = request.POST.get("verification_code")
            saved_code = request.session.get("verification_code")
            user_data = request.session.get("pending_user")

            if not user_data:
                return redirect("auth")

            if input_code == saved_code:
                user = User.objects.create_user(
                    email=user_data["email"],
                    password=user_data["password"],
                    first_name=user_data["first_name"],
                    last_name=user_data["last_name"],
                )
                login(request, user)

                request.session.flush()
                return redirect("home")

            return render(request, "verify_code.html", {"error": "Kod noto‘g‘ri"})

        if "login_submit" in request.POST:
            email = request.POST.get("email")
            password = request.POST.get("password")

            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect("home")

            return render(request, self.template_name, {"error": "Login yoki parol xato"})

        return render(request, self.template_name)


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("auth")

