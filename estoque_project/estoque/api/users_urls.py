from django.urls import path

from .. import views

app_name = "user"

urlpatterns = [
    path("", views.ProfileView.as_view(), name="index"),
    path("new/", views.UserNewView.as_view(), name="new"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("orders/", views.MyOrdersList.as_view(), name="my-orders"),
    path("orders/<int:pk>/", views.MyOrdersDetailView.as_view(), name="detail-order"),
]
