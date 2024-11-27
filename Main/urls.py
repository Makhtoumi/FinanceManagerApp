from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from Main import views
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
from django.conf import settings




urlpatterns = [
    path('', views.coslogin, name='login'),
    path('index/', views.mainpage, name='mainpage'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('set_balance/', views.set_balance, name='set_balance'),
    path('add_transaction/', views.add_transaction, name='add_transaction'),
    path('increase_balance/', views.increase_balance, name='increase_balance'),
    path('decrease_balance/', views.decrease_balance, name='decrease_balance'),
    path('add_u/',views.add_unit,name='add_unit'),
    path('add_soucat/',views.add_scategorie,name='add_scategorie'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('delete/categorie/<int:categorie_id>', views.delete_categorie, name='delete_categorie'),
    path('delete/souscategorie/<int:souscategorie_id>', views.delete_souscategorie, name='delete_souscategorie'),
    path('increase_balance/delete/<int:his_id>', views.delete_his_i, name='delete_his_i'),
    path('decrease_balance/delete/<int:his_id>', views.delete_his_d, name='delete_his_d'),







] 