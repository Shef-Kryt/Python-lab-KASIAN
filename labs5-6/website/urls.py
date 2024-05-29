from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('record/<int:pk>/', views.customer_record, name='record'),
    path('delete_record/<int:pk>/', views.delete_record, name='delete_record'),
    path('add_record/', views.add_record, name='add_record'),
    path('update_record/<int:pk>/', views.update_record, name='update_record'),
    path('search_records/', views.search_records, name='search_records'),
    path('record/<int:pk>/', views.customer_record, name='record_detail'),
    path('add_keyword/', views.add_keyword, name='add_keyword'),
    path('update_keyword/<int:pk>/', views.update_keyword, name='update_keyword'),
    path('save_keywords_to_json/', views.save_keywords_to_json, name='save_keywords_to_json'),
]

