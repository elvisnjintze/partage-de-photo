"""
URL configuration for fotoblog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
import authentication.views
import blog.views
urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', authentication.views.login_page, name='login'),
    path('', authentication.views.LoginPageView.as_view(), name='login'),
    path('logout', authentication.views.logout_user, name='logout'),
    path('home/', blog.views.home, name='home'),
path('signup/', authentication.views.signup, name='signup'),
    path('blog/upload/', blog.views.photo_upload, name='photo-uploader'),
    path('uploadphotoprofil/', authentication.views.upload_photo_profil, name='photo-profil'),
    path('blog/create/', blog.views.blog_and_photo_upload, name='create-blog'),
    path('blog/<int:blog_id>', blog.views.view_blog, name='view-blog'),
    path('blog/<int:blog_id>/edit', blog.views.edit_blog, name='edit-blog'),
    path('blog/upload-multiples', blog.views.create_multiple_photos, name='multiple-photos-uploader'),
    path('blog/follow-user', blog.views.follow_users, name='follow-users')
]
#si nous sommes en mode developpement c-a-d DEBUG = True,
#nous ajoutons MEDIA_URL comme chemin d'accès au media
# attentioln ceci ne marche pas en production
#nous aurons besoin d'une autre configuration différente
if settings.DEBUG:
    urlpatterns  += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
