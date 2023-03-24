
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

app_name = 'SocialMedia'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('SocialMedia.urls')),
    path('users', include('users.urls')),
    path('chat/', include('chat.urls'))

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)