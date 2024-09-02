from django.urls import path
from django.contrib.auth import views as auth_views

from .views import auth, views

urlpatterns = [
    path("", views.index, name="index"),
    path("new", views.new, name="new"),
    path('listings/<int:pk>/', views.listings, name='listings'),

    path('categories', views.categories, name='categories'),
    path('category/<str:pk>/', views.category, name='category'),

    path('watchlist', views.watchlist, name='watchlist'),
    path('watchlist/<int:pk>/', views.watchlist, name='watchlist'),

    path('bid/<int:pk>/', views.bid, name='bid'),
    path('close/<int:pk>/', views.close, name='close'),    

    path('comment/<int:pk>/', views.comment, name='comment'),

    path("login/", auth.login_view, name="login"),
    path("logout/", auth.logout_view, name="logout"),
    path("register/", auth.register, name="register"),
]
