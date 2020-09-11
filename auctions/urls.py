from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("addlisting",views.addlisting,name="addlisting"),
    path("listings/<int:product_id>",views.listings,name="listings"),
    path("users/<str:username>",views.users,name="users"),
    path("category",views.categories,name="categories"),
    path("category/<str:category>",views.category,name="category"),
    path("listings/<int:product_id>/addtowishlist/<str:user>",views.wishlist,name="wishlist"),
    path("wishlist",views.viewwishlist,name="viewwishlist"),
    path("listings/<int:product_id>/deletefromwishlist",views.deletewishlist,name="deletewishlist"),
    path("listings/<int:product_id>/closeauction",views.closeauction,name="closeauction"),
    path("mywins",views.myproducts,name="mywins")
]
