from django.shortcuts import render

def chat(request, chat_id):
    return render(request, 'assessment/chat.html', {
        'chat_id': chat_id
    })