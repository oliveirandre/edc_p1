"""edc_p1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from app import views

urlpatterns = [
        path('', views.ligas, name='liga'),
        path('tabela', views.tabelas, name='tabelas'),
        path('index', views.ligas, name='liga'),
        path('clube', views.clube, name='clube'),
        path('jogador', views.jogador, name='jogador'),
        path('addLiga', views.addLiga, name='addLiga'),
        path('addLigaXML', views.addLigaXML, name='addLigaXML'),
        path('editar_club', views.edit_club, name='edit_club'),
        path('edits_club', views.edits_clube, name='edits_club'),
        path('delete_jogador', views.delete_jogador, name='delete_jogador'),
        path('feed', views.feed, name="feed"),
        path('editar_jogador', views.editar_jogador, name="editar_jogador"),
        path('edits_jogador', views.edits_jogador, name="edits_jogador"),
        path('new_clube', views.new_clube, name="new_clube"),
        path('news_clube', views.news_clube, name="news_clube"),
        path('delete_clube', views.delete_clube, name="delete_clube"),
        path('delete_liga', views.delete_liga, name="delete_liga"),
        path('novo_jogador', views.novo_jogador, name="novo_jogador"),
        path('new_jogador', views.new_jogador, name="new_jogador"),
        path('xslt_run', views.trya, name="xslt_run")
]
