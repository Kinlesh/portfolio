# chatbot/views.py
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import authenticate, login
from .models import User
from pymongo import MongoClient
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView

#---------------------------------------------------------------
# MongoDB bağlantısı
client = MongoClient("mongodb://localhost:27017/")
db = client["chatbot_db"]  # MongoDB'deki veritabanı adı
chat_collection = db["chat_logs"]  # Mesajları tutacak koleksiyon
#----------------------------------------------------------------
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():

            # Form verilerini alın
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']

            # Kullanıcıyı hashlenmiş şifre ile kaydet
            User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            return redirect('login')  # Kayıt sonrası giriş sayfasına yönlendir
    else:
        form = RegisterForm()
    return render(request, 'chatbot/register.html', {'form': form})
class LoginInterfaceView(LoginView):
    template_name = "chatbot/login.html"
    success_url = '/chatbot/chat/'  # Giriş sonrası chatbot sayfasına yönlendir



@method_decorator(login_required, name='dispatch')
class ChatbotView(TemplateView):
    template_name = "chatbot/chat.html"

    def post(self, request, *args, **kwargs):
        user_message = request.POST.get("message")

        # Kullanıcı mesajını MongoDB'ye kaydet
        chat_collection.insert_one({
            "username": request.user.username,
            "role": "user",
            "content": user_message
        })
        # Bot yanıtı
        bot_response = f"Bu sizin '{user_message}' yazınıza cevabımdır."
        # Bot yanıtını da MongoDB'ye kaydet
        chat_collection.insert_one({
            "username": "bot",
            "role": "bot",
            "content": bot_response
        })

        return render(request, self.template_name, {
            "user_message": user_message,
            "bot_response": bot_response
        })
class WelcomeView(TemplateView):
    template_name = "chatbot/welcome.html"
class LogoutView(TemplateView):
    template_name = "chatbot/logout.html"