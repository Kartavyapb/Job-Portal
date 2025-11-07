from django.urls import path
from jobapp import views


urlpatterns = [
    path('',views.home, name='home'),
    path('register/',views.user_registration),
    path('welcome/', views.welcome,name="welcome"),
    path('create-it-jobs/', views.create_it_jobs, name="create-it-jobs"),
    path('list_of_it_jobs/', views.list_of_it_jobs),
    path('update-it/<int:id>/',views.update_it_jobs),
    path('itdelete/<int:id>/',views.itdelete),
    path('delete-it/<int:id>/',views.delete_it_jobs),
    path('help/',views.help),
    path('contact/',views.contact),
    path('about/',views.about),
    
]
