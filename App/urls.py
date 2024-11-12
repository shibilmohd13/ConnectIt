from django.urls import path, include
from App import views
from inbox import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('inbox/', views.inbox, name='inbox'),
    path('login/', include('django.contrib.auth.urls')),
    path('send_message', views.sendMessage, name='send_message'),
    path('about', views.about, name='about'),
    path('delete_message/<str:customer_id>', views.deleteMessage, name='delete_message'),
    path('customers/<str:customer_id>', views.Customers, name='customers'),
    path('mark_message/', views.markAsRead, name='mark_message'),
    path('email', views.email, name='email'),
    path('autologout/', views.AutoLogoutUser, name='autologout'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)