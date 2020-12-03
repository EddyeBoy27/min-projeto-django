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
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from .forms import ProductForm, UserForm, LoginForm
from django.db.models import F
import sys
import json

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
class OrdersListView(LoginRequiredMixin, TemplateView):
    template_name = 'estoque/carrinho.html'
    model = Aprodutoinstancia

    def get_context_data(self, *args, **kwargs):
        context = super(OrdersListView, self).get_context_data(**kwargs)
        context['produtos'] = Aprodutoinstancia.objects.filter(
            aprinid_acli=self.request.user.id,
        )
        return context


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
class NewOrderView(LoginRequiredMixin, CreateView):

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            prod = Aproduto.objects.get(pk=kwargs['pk'])
            user_email = request.user
            user_cliente = User.objects.get(username=user_email)
            new_pedido = Apedido.objects.create(acliid=user_cliente)
            new_pedido.save()
            Aprodutoinstancia.objects.create(
                aprinid_acli=user_cliente,
                aprinid_apedi=new_pedido,
                aprinid_aprodid=prod,
                aprinval=prod.aprodvalor,
                aprinqnt=1
            )
            pedido_inst_qnt = Aprodutoinstancia.objects.filter(
                aprinid_acli_id=user_cliente,
                aprinid_apedi_id=new_pedido,
                aprinid_aprodid_id=prod,
            ).values()[0]
            return JsonResponse({'pedId':new_pedido.apediid, 'pedQnt': pedido_inst_qnt})
            # newprod = Aproduto.objects.get(pk=kwargs['pk'])
            # return render(request, self.template_name, {'prod': prod, 'ped': new_pedido_inst, 'pednum': new_pedido})


@method_decorator(login_required, name='dispatch')
class UpdateOrderView(LoginRequiredMixin, UpdateView):

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            pedi_id = json.loads(request.body)['data']['pediId']
            pedi_inst = Apedido.objects.get(pk=pedi_id)
            prod = Aproduto.objects.get(pk=kwargs['pk'])
            user_email = request.user
            user_cliente = User.objects.get(username=user_email)
            Aprodutoinstancia.objects.create(
                aprinid_acli=user_cliente,
                aprinid_apedi=pedi_inst,
                aprinid_aprodid=prod,
                aprinval=prod.aprodvalor,
                aprinqnt=1
            )
            pedido_inst_qnt = Aprodutoinstancia.objects.filter(
                aprinid_acli_id=user_cliente,
                aprinid_apedi_id=pedi_id,
                aprinid_aprodid_id=prod,
            ).values()[0]
            return JsonResponse({'pedQnt':pedido_inst_qnt})

    def put(self, request, *args, **kwargs):
        if request.method == 'PUT':
            ped_inst_pk = json.loads(request.body)['data']['pedInst']
            pedi_id = json.loads(request.body)['data']['pediId']
            pedi_inst = Apedido.objects.get(pk=pedi_id)
            prod = Aproduto.objects.get(pk=kwargs['pk'])
            user_email = request.user
            user_cliente = User.objects.get(username=user_email)
            Aprodutoinstancia.objects.filter(
                aprinid=ped_inst_pk['pedQnt'],
                aprinid_acli_id=user_cliente,
                aprinid_apedi_id=pedi_id,
                aprinid_aprodid_id=prod,
            ).update(
                aprinqnt=F("aprinqnt") + 1,
                aprinval=prod.aprodvalor + (prod.aprodvalor * F("aprinqnt")),
            )
            return JsonResponse({'data': 'lallaa'})


@method_decorator(login_required, name="dispatch")
class UpdateCarrinhoView(LoginRequiredMixin, UpdateView):
    model = Aprodutoinstancia

    def get(self, request, *args, **kwargs):
        if request.method=='GET':
            print('to no get tio')
            print(request.body)
            ped_inst_pk = json.loads(request.body)['data']['aprinid']
            user_email = request.user
            user_cliente = User.objects.get(username=user_email)
            ped_inst_updated = self.model.objects.filter(
                aprinid=ped_inst_pk,
                aprinid_acli=user_cliente,
            ).all()
            return JsonResponse({ 'qnt': ped_inst_updated.aprinqnt, 'value': ped_inst_updated.aprinval})

    def put(self, request, *args, **kwargs):
        if request.method=='PUT':
            ped_inst_pk = json.loads(request.body)['data']['aprinid']
            method = json.loads(request.body)['data']['method']
            ped_inst = Aprodutoinstancia.objects.get(pk=ped_inst_pk)
            user_email = request.user
            user_cliente = User.objects.get(username=user_email)
            if method == 'increase':
                Aprodutoinstancia.objects.filter(
                    aprinid=ped_inst_pk,
                    aprinid_acli=user_cliente,
                ).update(
                    aprinqnt=F("aprinqnt") + 1,
                    aprinval=(F("aprinqnt") * ped_inst.aprinid_aprodid.aprodvalor)
                )
                print("atualizado increase")
            elif method == 'decrease':
                Aprodutoinstancia.objects.filter(
                    aprinid=ped_inst_pk,
                    aprinid_acli=user_cliente,
                ).update(
                    aprinqnt=(F("aprinqnt") - 1),
                    aprinval=(F("aprinqnt") * ped_inst.aprinid_aprodid.aprodvalor)
                )
                print("atualizado decrease")
        return HttpResponse(status=200)


@method_decorator(login_required, name="dispatch")
class FinishOrderView(LoginRequiredMixin, UpdateView):
    model = Apedido

    def put(self, request, *args, **kwargs):
        user_email = request.user
        user_cliente = User.objects.get(username=user_email)
        pedi_id = json.loads(request.body)['data']['apediId']
        self.model.objects.filter(
            apediid=pedi_id,
            acliid=user_cliente,
        ).update(
            apedistatus=2,
        )
        return HttpResponse(status=200)


@method_decorator(login_required, name='dispatch')
class MyOrdersList(LoginRequiredMixin, ListView):
    model = Apedido

    def get_context_data(self, *args, **kwargs):
        context = super(MyOrdersList, self).get_context_data(**kwargs)
        user_email = self.request.user
        user_cliente = User.objects.get(username=user_email)
        context['pedidos'] = self.model.objects.filter(
            apedistatus=2,
            acliid=user_cliente.pk,
        ).all()
        return context


@method_decorator(login_required, name='dispatch')
class MyOrdersDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'estoque/order_detail.html'
    model = Aprodutoinstancia

    def get_context_data(self, *args, **kwargs):
        context = super(MyOrdersDetailView, self).get_context_data(**kwargs)
        context['order_list'] = self.model.objects.filter(
            aprinid_apedi=self.kwargs['pk']
        ).all()
        return context
        