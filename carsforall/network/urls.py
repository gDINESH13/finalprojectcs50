
from django.urls import path

from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
   # path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("index",views.index,name="index"),
    path("createlisting",views.createlisting,name="createlisting"),
    path("list/<int:list_id>",views.list,name="list"),
    path("wishlist",views.wishlist,name="wishlist"),
    path("add_remove_wishlist",views.add_remove_wishlist,name="add_remove_wishlist"),
    path("ask_for_rent",views.ask_for_rent,name="ask_for_rent"),
    path("notification",views.notification,name="notification"),
    path("decline",views.decline,name="decline"),
    path("statusofcars",views.statusOfCars,name="statusofcars"),
    path("accept",views.accept,name="accept"),
    path("endrent",views.endrent,name="endrent"),
    path("profile<int:profile_id>",views.profile,name="profile")
]
