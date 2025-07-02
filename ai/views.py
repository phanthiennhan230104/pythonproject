from django.shortcuts import render, redirect
from django.conf import settings
from groq import Groq
import os
import re

client = Groq(api_key=settings.GROQ_API_KEY)

def chatbot_view(request):
    history = request.session.get('chat_history', [])
    response = None

    if request.method == "POST":
        if request.POST.get("clear_history"):
            request.session['chat_history'] = []
            return redirect('ai:chatbot')

        # Xử lý chat như bình thường
        user_input = request.POST.get("user_input")
        messages = [{"role": "system", "content": "You are a helpful AI assistant."}]
        for item in history:
            messages.append({"role": "user", "content": item['user']})
            messages.append({"role": "assistant", "content": item['bot']})

        messages.append({"role": "user", "content": user_input})

        # Gọi API Groq
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=messages,
            temperature=0.7
        )

        bot_reply = completion.choices[0].message.content.strip()

        # Nếu có mã code ``` => định dạng lại thành <pre><code>
        if "```" in bot_reply:
            bot_reply = re.sub(r"```(?:\w+)?", "", bot_reply).strip()
            bot_reply = f"<pre><code>{bot_reply}</code></pre>"

        history.append({'user': user_input, 'bot': bot_reply})
        request.session['chat_history'] = history

        response = bot_reply

    return render(request, 'ai/chatbot.html', {"history": history})





