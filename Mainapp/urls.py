from django.urls import path
from . import views

app_name = 'Mainapp'
urlpatterns = [
    path('', views.MainAppView.as_view(), name='schedule'),
    path('roomfilter/<str:roomFilter>/', views.MainAppView.as_view(), name='schedule'),
    path('month/<int:year>/<int:month>/<str:roomFilter>/', views.MainAppView.as_view(), name='schedule'),
    path('month/<int:year>/<int:month>/<int:day>/<str:roomFilter>/', views.MainAppView.as_view(), name='schedule'),
    path('scheduleid/<int:scheduleid>/', views.MainAppView.as_view(), name='scheduleid'),
    path('scheduleid/<int:scheduleid>/<str:roomFilter>/', views.MainAppView.as_view(), name='scheduleid'),
    
    path('security/', views.SecurityApp.as_view(), name='security'),
    path('security/<int:year>/<int:month>/<int:day>/', views.SecurityApp.as_view(), name='security'),

    path('securityform/<int:scheduleid>/', views.SecurityAppForm, name='securityfinishform'),

    path('filter/<int:year>/<int:month>/<int:day>/', views.receive_checkbox, name='filter'),

    path('form/<str:colum>/<int:scheduleid>/<str:roomFilter>/', views.Form, name='form'),
    path('sealform/<int:year>/<int:month>/<int:day>/<int:scheduleid>/<str:roomFilter>/', views.DelForm, name='delform'),
]