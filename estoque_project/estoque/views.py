from django.views.generic import DetailView, ListView, UpdateView, CreateView
from django.views.generic import DeleteView, TemplateView, RedirectView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, reverse, redirect
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .forms import ProductForm, UserForm, LoginForm

from .models import Aproduto, Aprodutoinstancia, Apedido


@method_decorator(login_required, name='dispatch')
class ProdutoListView(ListView):
    template_name = 'estoque/aproduto_list.html'
    model = Aproduto

    def post(self, request, *args, **kwargs):
        email = request.POST.get('acliemail', '')
        password = request.POST.get('aclipass', '')
        if request.method == 'POST':
            try:
                actual_user = User.objects.get(acliemail=email)
            except:
                return redirect(reverse('login:login'))
            else:
                if password != actual_user.aclipass:
                    return redirect(reverse('login:login'))
            product = self.model.objects.all()
            return render(request, self.template_name, {'aproduto_list': product, 'user': email})


@method_decorator(login_required, name='dispatch')
class ProdutoDetailView(DetailView):
    template_name = 'estoque/aproduto_detail.html'
    model = Aproduto

    def post(self, request, *args, **kwargs):
        print(request.POST.get('acliemail'))
        if request.method == 'POST':
            form = ProductForm(request.POST)

            if form.is_valid():
                return HttpResponseRedirect(f"/produtos/{self.kwargs['pk']}/")
        return render(request, self.template_name, {'pk': self.kwargs['pk']})


@method_decorator(login_required, name='dispatch')
class ProdutoUpdateView(UpdateView):
    template_name = 'estoque/aproduto_form.html'
    model = Aproduto
    form_class = ProductForm
    success_url = '/produtos/'

    def get_object(self):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(Aproduto, aprodid=id_)

    def form_valid(self, form):
        return super(ProdutoUpdateView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class ProdutoCreateView(CreateView):
    template_name = 'estoque/aproduto_new.html'
    model = Aproduto
    form_class = ProductForm
    success_url = '/produtos/'

    def form_valid(self, form):
        return super(ProdutoCreateView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class ProdutoDeleteView(DeleteView):
    model = Aproduto
    success_url = '/produtos/'

    def form_valid(self, form):
        return super(ProdutoDeleteView, self).form_valid(form)


class UserNewView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'estoque/acliente_form.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        return super(UserNewView, self).form_valid(form)


class LoginView(LoginView):
    model = User
    template_name = 'estoque/login.html'
    form_class = LoginForm
    redirect_field_name = '/produtos/'

    def form_valid(self, form):
        return super(LoginView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class ProfileView(TemplateView):
    template_name = 'estoque/initial_page.html'


@method_decorator(login_required, name='dispatch')
class LogoutView(RedirectView):
    url = '/'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class NewOrderView(LoginRequiredMixin, TemplateView):
    template_name = 'estoque/orders_list.html'

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            prod = Aproduto.objects.get(pk=kwargs['pk'])
            user_email = request.user
            user_cliente = User.objects.get(username=user_email)
            new_pedido = Apedido.objects.create(acliid=user_cliente)
            new_pedido.save()
            new_pedido_inst = Aprodutoinstancia.objects.create(
                aprinid_acli=user_cliente,
                aprin_apedi=new_pedido,
                aprinval=prod.aprodvalor,
                aprinqnt=1
            )
            new_pedido_inst.save()
            # newprod = Aproduto.objects.get(pk=kwargs['pk'])
            return render(request, self.template_name, {'prod': prod, 'ped': new_pedido_inst, 'pednum': new_pedido})


@method_decorator(login_required, name='dispatch')
class UpdateOrderView(LoginRequiredMixin, TemplateView):
    template_name = 'estoque/orders_list.html'

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            print(request.body)
            print(args)
            print(kwargs)
            prod = Aproduto.objects.get(pk=kwargs['pk'])
            user_email = request.user
            user_cliente = User.objects.get(username=user_email)
            
            return render(request, self.template_name, {'prod': prod, 'ped': 1})

