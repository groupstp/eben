from django.http.response import HttpResponse
from django.shortcuts import render
from eben.chat.models import Dialog, User_to_dialog, Message, Message_to_user
from eben.users.models import User
from django.db.models import Q
import datetime

def messager(request):
    """
    Выводит список диалогов пользователя и сообщения заданного диалога
    """
    #выбираем пользователя
    user = request.user
    if user.is_active:
        user_to_dialog = User_to_dialog.objects.filter(user_id = user.id)
        dialogs = get_dialogs_to_user(user.id)
        #выбор диалога
        #dialog = user_to_dialog[0].dialog_id
        #messages = Message.objects.filter(dialog_id = dialog).order_by("time")
        #users = users_by_dialog(dialog)
        #num_new_mes_dialog = num_new_messages_to_dialogs(user_to_dialog)
        
        return render(request, 'chat/messager.html', {'user': user, 
                               'dialogs': dialogs})
    else:
        return HttpResponse("By!") 

'''
def messager(request):
    user = request.user
    if user.is_active:
        return HttpResponse(user.id)
    else:
        return HttpResponse("By!")
'''

def get_num_new_message(request):
    """
    Получить кол-во не прочитанных сообщений
    """
    user = request.user
    if user.is_active:
        num_new_message = len(Message_to_user.objects.filter(Q(user_id = user.id) & Q(status = False)))
        return HttpResponse(num_new_message)
    else:
        return HttpResponse("By!")


def get_dialogs_to_user(user_id):
    """
    Получить список дилогов пользователя
    """
    user_to_dialog = User_to_dialog.objects.filter(user_id = user_id) 
    dialogs = []
    for dialog in user_to_dialog:
        dialogs += [dialog.dialog]
    return dialogs


def get_message(request):
    """
    Получить список сообщений диалога.
    Метод возвращает 50 сообщений
    """

    dialog_id = request.POST['dialog_id']
    list = request.POST['list']
    dialog = Dialog.objects.get(id = dialog_id)

    step = 50
    num = len(Message.objects.filter(dialog_id = dialog.id))
    if num > request.POST['list'] * step:
        messages = Message.objects.filter(dialog_id = dialog.id). \
                       order_by('time')[list * step: (1 + list) * step]
    else:
        messages = Message.objects.filter(dialog_id=dialog.id). \
                       order_by('time')[list * step: num]

    return HttpResponse(messages)


def num_new_messages_to_dialogs(user_to_dialog):
    """
    Возвращает словарь диалогов с кол-вом не прочитанных сообщений
    """
    num_new_mes_dialog = {}
    for dialog in user_to_dialog:
        if dialog.num_new_mes > 0:
            num_new_mes_dialog.update({dialog.dialog.id: dialog.num_new_mes})
    return num_new_mes_dialog


def users_by_dialog(dialog_id):
    """
    Получить список пользователей диалога
    """
    users_to_dialog = User_to_dialog.objects.filter(dialog_id = dialog_id)
    users = []
    for obj in users_to_dialog:
        user = User.objects.get(id = obj.user_id)
        users += [user]

    return users


def del_message(request):
    """
    Удалить сообщение для пользователя,
    если все пользователи удалили сообщение, то оно удаляется из БД
    """
    message_id = request.POST['message_id']
    user_id = request.POST['user_id']
    user_to_message = Message_to_user.objects.filter(user_id = user_id).get(message_id = message_id)
    user_to_message.status_del = True
    user_to_message.save()

    user_to_messages = Message_to_user.objects.filter(message_id = message_id)
    f = True
    for obj in user_to_messages:
        if obj.status_del == False:
            f = False
    if f:
        user_to_messages.delite()
        m = Message.objects.get(id = message_id)
        m.delite()


def del_dialog(request):
    """
    Удаленире диалога мользователем,
    если сообщений в диалоге нету, то все записи из БД удаляются
    """
    user_id = request.POST['user_id']
    dialog_id = request.POST['dialog_id']
    messages = Message.objects.filter(dialog_id = dialog_id)
    for message in messages:
        del_message(message.id, user_id)
    if messages == None:
        u = User_to_dialog.objects.filter(dialog_id = dialog_id)
        u.delite()
        d = Dialog.objects.get(id = dialog_id).delite()
        d.delite()


def new_dialog(request):
    """
    Записывает данные нового диалога в БД
    """
    user = request.user.id
    user = User.objects.get(id=user)
    users = request.GET['user_id']
    users = User.objects.get(id=users)
    dialog = Dialog(name=users.name ,user=user)
    dialog.save()
    #date = datetime.now(tz=None)
    date = 11111111
    user1_to_dialog = User_to_dialog(user=users, dialog_id=dialog.id, time=date)
    user2_to_dialog = User_to_dialog(user=user, dialog_id=dialog.id, time=date)
    user1_to_dialog.save()
    user2_to_dialog.save()
    return HttpResponse(dialog.id)

def new_group_dialog(request):
    """
    Метод создает новый групповой диалог
    """
    users_id = request.POST['users_id']
    dialog = Dialog(user=users_id[0])
    dialog.save()
    for user_id in users_id:
        user_to_dialog = User_to_dialog(user=user_id, dialog_id=dialog.id, time=date)
        user_to_dialog.save()
    return dialog.id

def add_user_to_dialog(request):
    """
    Добавляем пользователя в групповой диалог и даем доступ ко всем сообщениям диалога
    """
    user_id = request.POST['user_id']
    dialog_id = request.POST['dialog_id']
    new_user_to_dialog = User_to_dialog(user=user_id, dialog_id=dialog_id, time=datetime.now(tz=None))
    new_user_to_dialog.save()
    messages = Message.objects.filter(dialog_id=dialog_id)
    for message in messages:
        m_t_u = Message_to_user(message_id=message.id, user_id=user_id, status=True, status_del=False)
        m_t_u.save()


def new_message(request):
    """
    Добавляем новое сообщение в БД
    """
    sender_id = request.user.id
    time = datetime.now(tz=None)
    text = request.POST['text']
    dialog_id = request.POST['dialog_id']

    message = Message(message=text, sender_id=sender_id, dialog_id=dialog_id, status=False, status_del=False,
                      time=time)
    message.save()
    users = users_by_dialog(dialog_id)
    for user in users:
        if sender_id == user.id:
            m_t_u = Message_to_user(message_id=message.id, user_id=user.id, status=True, status_del=False)
            m_t_u.save()
        else:
            m_t_u = Message_to_user(message_id=message.id, user_id=user.id, status=False, status_del=False)
            m_t_u.save()


def read_message(request):
    """
    Метод отмечает сообщение, как прочитанное
    """
    message_id = request.POST['message_id']
    message = Message.objects.get(id = message_id)
    message.status = True
    message_to_user = Message_to_user.object.get(message = message.id)
    message_to_user.status = True
    message.save()
    message_to_user.save()













