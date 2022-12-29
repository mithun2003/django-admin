from django.urls import path
from . import views
urlpatterns = [
    path('',views.loginPage,name='login'),      
    path('register',views.registerPage,name='register'),      
    path('logout/',views.logoutUser,name='logout'),      
    path('home',views.index,name='home'),      
    path('about',views.about,name='about'),
    path('contact',views.contact,name='contact'),
    path('post',views.post,name='post'),
    path('admin/', views.admin_login,name='admin1'),
    path('admin/showusers', views.show_users,name='showuser'),
    path('admin/user_edit!<id>',views.edit_user,name='edit_user'),
    #path('admin/view', views.edit_user,name='view'),
     #path('admin/save', views.save),
    path('admin/user_delete!<id>', views.delete_user,name='delete'),
    path('admin/make', views.make,name='make'),
    path('admin/logout', views.logoutad,name='logoutad'),
    path('admin/search', views.searched_user),
    path('admin/create', views.create, name='create')
]
