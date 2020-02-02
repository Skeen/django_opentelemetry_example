from django.shortcuts import render

def index(request):
    from django.contrib.auth import get_user_model
    print(get_user_model().objects.all())
    return render(request, 'chat/index.html', {})

def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })
