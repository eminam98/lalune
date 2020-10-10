from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
import json
from django.views import generic
from django.views.generic import View
from .forms import UserForm
from .forms import UserUpdateForm, ProfileUpdateForm
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from .models import *
import datetime
from django.template.loader import render_to_string



def home(request):
    return render(request, 'LaLune/home.html', {'title': 'Pocetna'})

def galerija(request):
    return render(request, 'LaLune/galerija.html', {'title': 'Galerija'})


def contact(request):
    if request.method == "POST":
        ime = request.POST['ime']
        mail = request.POST['mail']
        poruka = request.POST['poruka']

        send_mail(ime,poruka,mail,['cosmeticslalune@gmail.com', mail],)

        return render(request, 'LaLune/kontakt.html', {'ime':ime})

    else:
        return render(request, 'LaLune/kontakt.html', {'title': 'Kontakt'})



def about(request):
    return render(request, 'LaLune/onama.html', {'title': 'O nama'})


def faq(request):
    return render(request, 'LaLune/faq.html', {'title': 'FAQ'})


def politika(request):
    return render(request, 'LaLune/politika.html', {'title': 'FAQ'})


def naruciti(request):
    return render(request, 'LaLune/naruciti.html', {'title': 'Kako naruciti'})


class UserFormView(View):
    form_class = UserForm
    template_name='LaLune/registracija.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user=authenticate( username=username, password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect('profil')

        return render(request, self.template_name, {'form': form})



@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profil')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'LaLune/profile.html', context)


def store(request):
    if request.user.is_authenticated:
        customer = request.user.profile
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']
    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems, 'shipping':False}
    return render(request, 'LaLune/proizvodi.html', context)


def oci(request):
    products = Product.objects.all().filter(kategorija='Oci')
    context = {'products': products,
               'rijec': "Oci",}
    return render(request, 'LaLune/proizvodi.html', context)


def lice(request):
    products = Product.objects.all().filter(kategorija='Lice')
    context = {'products': products,
               'rijec': "Lice",}
    return render(request, 'LaLune/proizvodi.html', context)


def usne(request):
    products = Product.objects.all().filter(kategorija='Usne')
    context = {'products': products,
               'rijec': "Usne",}
    return render(request, 'LaLune/proizvodi.html', context)


def cart(request):

    if request.user.is_authenticated:
        customer = request.user.profile
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items':0, 'shipping':False}


    context = {'items': items, 'order': order}
    return render(request, 'LaLune/korpa.html', context)




def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.profile
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping':False}

    context = {'items': items, 'order': order}
    return render(request, 'LaLune/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId =data['productId']
    action = data['action']

    print('Action:', action)
    print('ProductId:', productId)

    customer = request.user.profile
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product= product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action =='remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Dodano u korpu!', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    user = request.user

    if request.user.is_authenticated:
        customer = request.user.profile
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()
        context = {
            'user': user,
            'items': items,
            'order': order
        }
        subject ='Hvala Vam na narudzbi!'
        message = render_to_string('LaLune/email_template.html', context)
        from_email= settings.EMAIL_HOST_USER
        to_list=[user.email, settings.EMAIL_HOST_USER]
        send_mail(subject, message, from_email, to_list, fail_silently=True)


        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                adresa=data['shipping']['address'],
                grad=data['shipping']['city'],
                postanskibroj=data['shipping']['zipcode'],
                drzava=data['shipping']['country'],
            )

    else:
        print('Korisnik nije prijavljen')
    return JsonResponse('Payment complete!', safe=False)


