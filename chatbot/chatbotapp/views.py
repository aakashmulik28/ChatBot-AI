from django.shortcuts import render
from django.http import JsonResponse
from .models import ChatMessage
from dotenv import load_dotenv
import os

import google.generativeai as genai   # ✅ Correct import
import google.generativeai as genai
genai.configure(api_key="***aSyA1mWeDs-***EWQTGAK6E3Bbh4X*********")


for m in genai.list_models():
    print(m.name, m.supported_generation_methods)


# Load environment variables
load_dotenv() 
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))   # ✅ Configure once

from django.shortcuts import render
from .models import ChatMessage

def home(request):
    history = ChatMessage.objects.order_by('-timestamp')[:20]  # last 20 messages
    return render(request, 'chatbotapp/home.html', {'history': history})

# Clear history
def clear_history(request):
    ChatMessage.objects.all().delete()
    return JsonResponse({'status': 'cleared'})




def get_response(request):
    user_msg = request.GET.get('msg')
    print("📩 Received message:", user_msg)

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")  # supported model
        response = model.generate_content(user_msg)

        print("✅ Gemini response object:", response)
        bot_msg = response.text if response and response.text else "No reply from Gemini"
        print("💬 Bot reply:", bot_msg)

    except Exception as e:
        print("🚨 Gemini error:", repr(e))
        bot_msg = "AI service not available right now."

    try:
        ChatMessage.objects.create(user_message=user_msg, bot_response=bot_msg)
        print("✅ Saved to database")
    except Exception as e:
        print("🚨 Database save error:", repr(e))

    return JsonResponse({'bot_response': bot_msg})


