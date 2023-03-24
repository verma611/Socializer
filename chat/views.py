from django.shortcuts import render, get_object_or_404
import json
from .models import Friend, Message
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.utils.timezone import localtime


from django.db.models import Q


@login_required
def friend_list(request):
    user = request.user
    friends = Friend.objects.filter(Q(from_user=user) | Q(to_user=user))
    return render(request, 'friend_list.html', {'friends': friends})

@login_required
def chat_history(request, friend_id):
    friend = get_object_or_404(Friend ,pk=friend_id)
    print(friend)

    messages = Message.objects.filter(
        Q(sender=friend.from_user, receiver=friend.to_user) | Q(sender=friend.to_user, receiver=friend.from_user)
    ).order_by('timestamp').prefetch_related('sender', 'receiver')

    messages_list = []
    for message in messages:
        message_dict = {
            'content': message.content,
            'timestamp': localtime(message.timestamp).strftime('%b %d, %Y %I:%M %p'),
            'sender': message.sender,
            'receiver': message.receiver,
            'is_current_user': message.sender == request.user
        }
        messages_list.append(message_dict)

    return render(request, 'chat_history.html', {'friend': friend, 'messages': messages_list})

@login_required
@require_POST
def send_message(request, friend_id):
    friend = get_object_or_404(Friend, pk=friend_id)
    
    content = json.loads(request.body)['message']

    reciver_name = ""
    if request.user == friend.to_user:
        reciver_name = friend.from_user
    elif request.user != friend.to_user:
        reciver_name = friend.to_user

    message = Message.objects.create(sender=request.user, receiver=reciver_name, content=content)
    message.clean()

    
    message.save()
    
    messages = Message.objects.filter(
        Q(sender=friend.from_user, receiver=friend.to_user) | Q(sender=friend.to_user, receiver=friend.from_user)
    ).order_by('timestamp').prefetch_related('sender', 'receiver')

    messages_list = list(messages.values('content', 'timestamp', 'sender_id', 'receiver_id'))
    for message in messages_list:
        message['is_sender'] = message['sender_id'] == request.user.id
        message['timestamp'] = localtime(message['timestamp']).strftime('%b %d, %Y %I:%M %p')
        del message['sender_id']
        del message['receiver_id']

    return JsonResponse({
        'success': True,
        'friend': friend.to_dict(),
        'messages': messages_list
    })

def chat_home(request):
    return render(request, "chat.html")
