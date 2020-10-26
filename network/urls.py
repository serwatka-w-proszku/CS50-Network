from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = "network"

urlpatterns = [
    path("", views.index, name="index"),
    path("user_profile/<int:user_id>", views.user_profile, name="user_profile"),
    path("following", views.following, name="following"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
