
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


# defining our url to the server for all apps of our websites
urlpatterns = [
    path('admin/', admin.site.urls),
    
    # this is the url for our mini app base
    path('', include('base.urls')),
    
    # this is the for recognizing and connecing with our api
    path('api/', include('base.api.urls')),
    
    path('api-auth/', include('rest_framework.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)