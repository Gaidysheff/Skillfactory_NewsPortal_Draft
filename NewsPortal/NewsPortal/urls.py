"""NewsPortal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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


from django.contrib import admin
from django.urls import path, re_path

from newsapp.views import index, archive, categories, pageNotFound, about


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),
    path('about/', about, name='about'),
    path('cats/<slug:cat>/', categories, name='cats'),
    re_path(r'^archive/(?P<year>[0-9]{4})/', archive, name='archive'),
]

handler404 = pageNotFound

# --------------------------------------------------------------------------------
# Этот код только на время отладки работы с медиа-файлами (пока DEBUG=True)

from django.conf.urls.static import static
from django.conf import settings

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

