from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),
    path('politika/', views.politika, name='politika'),
    path('naruciti/', views.naruciti, name='naruciti'),
    path('register/', views.UserFormView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='LaLune/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='LaLune/logout.html'), name='logout'),
    path('profile/', views.profile, name='profil'),
    path('contact/', views.contact, name='kontakt'),
    path('galerija/', views.galerija, name='galerija'),
    path('proizvodi/', views.store, name="proizvodi"),
    path('oci/', views.oci, name="oci"),
    path('lice/', views.lice, name="lice"),
    path('usne/', views.usne, name="usne"),
    path('korpa/', views.cart, name="korpa"),
    path('checkout/', views.checkout, name="checkout"),
    path('proizvodi/update_item/', views.updateItem, name="update_item"),
    path('korpa/update_item/', views.updateItem, name="update_item"),
    path('oci/update_item/', views.updateItem, name="update_item"),
    path('usne/update_item/', views.updateItem, name="update_item"),
    path('lice/update_item/', views.updateItem, name="update_item"),
    path('checkout/process_order/', views.processOrder, name="process_order"),


]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

