"""
URL configuration for Webapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from disasterpredictor import views
from django.contrib.auth import views as auth_views
from disasterpredictor.views  import explain_graph

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("worldmap/", views.worldmap, name="worldmap"),
    path("country/", views.country_analysis, name="country"),

    # custom login/logout/signup
    path("login/", views.custom_login, name="login"),
    path("logout/", views.custom_logout, name="logout"),
    path("signup/", views.signup, name="signup"),

    # password reset
    path("reset_password/", auth_views.PasswordResetView.as_view(), name="reset_password"),
    path("reset_password_sent/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset_password_complete/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    #explain graph
    path("explain-graph/", explain_graph, name="explain_graph"),

]
