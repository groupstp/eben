from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.messager, name="messager"), #вывести диалоги
    url(r'^num-new-messages/$', views.get_num_new_message), #получить кол-во новых сообщений
    url(r'^get-messages-to-dialog/$', views.get_message), #прлучить сообщения диалога
    url(r'^new-message/$', views.new_message), #скрипт отправки сообщения
    url(r'^read-message/$', views.read_message), #скрипт прочтения сообщения
    url(r'^add-user-to-dialog/$', views.add_user_to_dialog), #Скрипт добавления нового участника к диалогу
    url(r'^new-group-dialog/$', views.new_group_dialog), #Скрипт создания нового группового диалога
    url(r'^new-dialog/$', views.new_dialog), #Скрипт создания нового диалога
    url(r'^del-dialog/$', views.del_dialog), #Скрипт удаления диалога пользователем
    url(r'^del-message/$', views.del_message), #Скрипт удаления соощения
    url(r'^dialogs/$', views.dialogs)] #Скрипт получения списка диалогов
