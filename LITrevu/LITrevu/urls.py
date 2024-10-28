"""
URL configuration for LITrevu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView)
from django.urls import include, path

import authentication.views
import blog.views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [

    path("__reload__/", include("django_browser_reload.urls")), # a supprimer en fin de projet



    path('admin/', admin.site.urls),
    path('', LoginView.as_view(
        template_name='authentication/login.html',
        redirect_authenticated_user=True),
         name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', PasswordChangeView.as_view(
        template_name='authentication/password_change_form.html'),
         name='password_change'
         ),
    path('change-password-done/', PasswordChangeDoneView.as_view(
        template_name='authentication/password_change_done.html'),
         name='password_change_done'
         ),
    path('signup/', authentication.views.signup_page, name='signup'),
    path('home/', blog.views.home, name='home'),
    path('ticket/create/', blog.views.create_ticket, name='create_ticket'),
    path('ticket/update/<int:ticket_id>', blog.views.update_ticket, name='update_ticket'),
    path('ticket/delete/<int:ticket_id>', blog.views.delete_ticket, name='delete_ticket'),
    path('review/create/<int:ticket_id>', blog.views.create_review, name='create_review'),
    path('review/update/<int:review_id>', blog.views.update_review, name='update_review'),
    path('review/delete/<int:review_id>', blog.views.delete_review, name='delete_review'),
    path('ticket_and_review/create/', blog.views.create_ticket_and_review, name='create_ticket_and_review'),
    path('user/reviews/', blog.views.user_reviews, name='user_reviews'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)