from django.urls import path

from .. import views

app_name = "produto"

urlpatterns = [
    path("", views.ProdutoListView.as_view(), name="list"),
    path(
        "<int:pk>/",
        views.ProdutoDetailView.as_view(),
        name="detail"
    ),
    path("<int:pk>/edit/", views.ProdutoUpdateView.as_view(), name="update"),
    path("new/", views.ProdutoCreateView.as_view(), name="create"),
    path("<int:pk>/delete/", views.ProdutoDeleteView.as_view(), name="delete"),
    path("orders/add/<int:pk>/", views.NewOrderView.as_view(), name="add_order"),
    path("orders/update/<int:pk>/", views.UpdateOrderView.as_view(), name="update_order"),
]
