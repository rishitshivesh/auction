from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms

from .models import User,AuctionListings,Categories,Comments,Wishlist,Bids


class place_bid(forms.Form):
    bid = forms.IntegerField(label="", widget=forms.TextInput(attrs={'placeholder': 'Enter your bid here','class':'form-control mx-auto w-50 p-3'}))


class comment_form(forms.Form):
    comment = forms.CharField(label="", max_length=500, widget=forms.Textarea(attrs={'placeholder':'Comment Here','class':'form-control h-50 d-inline-block','rows':'3'}))


def index(request):
    bids = Bids.objects.all()
    return render(request, "auctions/index.html",{
        "bid" : bids,
        "listings" : AuctionListings.objects.all(),
        "count" : 0,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["firstname"]
        last_name = request.POST["lastname"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name=first_name
            user.last_name=last_name
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url='login')
def listings(request,product_id,):
    product = AuctionListings.objects.get(pk=product_id)
    adder = User.objects.get(username=product.bid_user)
    message = None
    msgtype= None
    if request.method=="POST":
        form = place_bid(request.POST)
        commentform = comment_form(request.POST)
        if form.is_valid():
            bid = form.cleaned_data["bid"]
            bid_model = Bids.objects.get(product=product)
            if int(bid_model.bid) < int(bid):
                bid_model.user = request.user
                bid_model.product = product
                bid_model.bid = bid
                bid_model.save()
                wishlistadd = Wishlist(product=product,user=request.user)
                wishlistadd.save()
                message = "Bid Placed Successfully!"
                msgtype = "success"
            else : 
                message = "Your Bid Should be higher than previous Bid"
                msgtype= "warning"
        
        elif commentform.is_valid():
            comment = commentform.cleaned_data["comment"]
            c = Comments(user=request.user, product=product, comment=comment)
            c.save() 
        else:
            bids = Bids.objects.get(product=product)
            return render(request, "auctions/description.html",{
                "product": product,
                "bid": bids,
                "adder" : adder,
                "form": place_bid(),
                "comment" : comment_form(),
                "message": message,
                "comments" : Comments.objects.filter(product=product).order_by('-date'),
                "status" : status
                })

    # if request.method=="POST":
    #     comment = Comments(comment=request.POST["comment"],user=request.POST["username"],product_id=product_id)
    #     #product = AuctionListings.objects.get(id=product_id).id
    #     #comment.product_id.add(product)
    #     #comment.user.add(request.POST["username"])
    #     comment.save()
    #     return HttpResponseRedirect(reverse("listings", args =(product_id,)))
    else:
        pass
    print(product.product_type)
    # if product:
    #status = None
    bids = Bids.objects.get(product=product)
    if Wishlist.objects.filter(user=request.user,product=product):
        status = True
    else:
        status=False
    return render(request,"auctions/products.html",{
            "bid": bids,
            "form": place_bid(),
            "adder" : adder,
            "product" : product,
            "comment" : comment_form(),
            "comments" : Comments.objects.filter(product=product).order_by('-date'),
            "status" : status,
            "message" : message,
            "type" : msgtype,
        })
        # else:
        #      return render(request,"auctions/error.html",{
        #         "message" : "Product Not Found!!",
        #     })




# @login_required(login_url='login')
# def listings(request,product_id):
#     product = AuctionListings.objects.get(pk=product_id)
#     if request.method=="POST":
#         comment = Comments(comment=request.POST["comment"],user=request.POST["username"],product_id=product_id)
#         #product = AuctionListings.objects.get(id=product_id).id
#         #comment.product_id.add(product)
#         #comment.user.add(request.POST["username"])
#         comment.save()
#         return HttpResponseRedirect(reverse("listings", args =(product_id,)))
#     else:
#         # if product:
#         #status = None
#         bids = Bids.objects.get(product=product)
#         if Wishlist.objects.filter(user=request.user,product=product):
#             status = True
#         else:
#             status=False
#         return render(request,"auctions/products.html",{
#                 "bid": bids,
#                 "form": place_bid(),
#                 "product" : product,
#                 "comments" : Comments.objects.filter(product_id=product_id).order_by('-date'),
#                 "status" : status,
#                 "message": "Your bid should be higher than the previous Bid",
#         })
#         # else:
#         #      return render(request,"auctions/error.html",{
#         #         "message" : "Product Not Found!!",
#         #     })

# def bid(request,product_id):
#     form = place_bid(request.POST)
#     product = AuctionListings.objects.get(pk=product_id)
#     if request.method=="POST":
#         if form.is_valid():
#             bid = request.POST.get("bid")
#             bid_model = Bids.objects.get(product=product)
#             if int(bid_model.bid) < int(bid):
#                 bid_model.user = request.user
#                 bid_model.product = product
#                 bid_model.bid = bid
#                 bid_model.save()
#             else:
#                 pass
#     listings(request,product_id)
#                 # return render(request, "auctions/description.html",{
#                 #     "product": product,
#                 #     "bid": bids,
#                 #     "form": place_bid(),
#                 #     "message": "Your bid should be higher than the previous Bid",
#                 #     "comments" : Comments.objects.filter(product_id=product_id).order_by('-date'),
#                 #     "status" : status
#                 #     }) 


def category(request,category):
    return render(request, "auctions/category.html",{
        "listings" : AuctionListings.objects.filter(product_type=category),
        "category" : category,
    })
def categories(request):
    return render(request, "auctions/categories.html",{
        "listings" : Categories.objects.all(),
    })
@login_required(login_url='login')    
def addlisting(request):
    if request.method == "POST":
        product_name = request.POST["product_name"]
        description = request.POST["description"]
        price = request.POST["price"]
        product_type = request.POST["product_type"]
        # bids = request.POST["bids"]
        bid_user = request.POST["username"]
        url = request.POST["url"]
        if(url):
            URL = url
        else:
            URL = "https://icon-library.com/images/products-icon-png/products-icon-png-25.jpg"
 #       category=Categories.objects.filter(id=request.POST["category"])
        product = AuctionListings(product_name=product_name,description=description,product_type=product_type,price=price,bid_user=bid_user,url=URL)
        #product.category.add(category)
        product.save()
        bid = Bids(product=product,user=request.user,bid=product.price)
        bid.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/addlisting.html",{
            "categories" : Categories.objects.order_by('category')
        })
@login_required(login_url='login')  
def users(request,username):
    user = User.objects.get(username=username)
    return render(request, "auctions/user.html",{
        "listings" : AuctionListings.objects.filter(bid_user=username).all(),
        "bid_user" : user,
        "message" : "Active Listings",
    })
@login_required(login_url='login')
def wishlist(request,user,product_id):
    Product = AuctionListings.objects.get(pk=product_id)
    if request.method=="POST":
        wishlist = Wishlist.objects.filter(product=Product,user=request.user)
        print(wishlist)
        if Wishlist.objects.filter(product=Product,user=request.user).exists() :
            return HttpResponseRedirect(reverse('viewwishlist'))
        else:
            # wishlist.product.add(Product)
            # wishlist.user.add(Users)
            if request.user.username==user:
                wishlistadd = Wishlist(product=Product,user=request.user)
                wishlistadd.save()
                return HttpResponseRedirect(reverse('index'))
            else:
                pass
  

@login_required(login_url='login')
def viewwishlist(request):
    return render(request, "auctions/viewwishlist.html",{
        "listings" : Wishlist.objects.filter(user=request.user).all(),
        "bid_user" : request.user.username,
    })

@login_required(login_url='login')
def deletewishlist(request,product_id):
    product = AuctionListings.objects.get(pk=product_id)
    wishlist = Wishlist.objects.get(product=product,user=request.user).delete()
    return HttpResponseRedirect(reverse('listings',args=(product_id,)))

@login_required(login_url='login')
def closeauction(request,product_id):
    product = AuctionListings.objects.get(pk=product_id)
    if request.user.username == product.bid_user:
        product.listed=False
        product.save()
    return HttpResponseRedirect(reverse('index'))

def myproducts(request):
    products = Bids.objects.filter(user=request.user)
    return render(request, "auctions/myproducts.html",{
        "listings" : products
    })