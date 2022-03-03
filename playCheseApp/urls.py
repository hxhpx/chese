from django.conf.urls import url, include
from . import views
from . import newViews

urlpatterns = [
    url(r'make_size', views.make_size,),
    #url(r'getpiecearray', views.get_piece_array,),
    url(r'sendPos', views.sendPos, ),
    url(r'restart',views.restart,),
    url(r'checkend', views.checkEnd,),
    url(r'sendpos', views.sendHistory,),
    url(r'getid',newViews.getID,),
    url(r'review',newViews.review,),
    url(r'start',views.make_size,),
    url(r'keeptest', newViews.keep,),
    url(r'board', newViews.board,),
]