from django.contrib import admin
from .models import AuctionListings, Bids, Comments, Categories,User
# Register your models here.

class BidsAdmin(admin.ModelAdmin):
    list_display = ("id","product","user","bid")
class ListingAdmin(admin.ModelAdmin):
    list_display = ("id","product_name","bid_user","date","price","listed","product_type")
class CommentAdmin(admin.ModelAdmin):
    list_display = ("product","user","date")
class UserDisplay(admin.ModelAdmin):
    list_display = ("id","first_name","last_name","username")
# class PassengerAdmin(admin.ModelAdmin):
#     filter_horizontal = ("flights",)

admin.site.register(AuctionListings,ListingAdmin)
# admin.site.register(Flight, FlightAdmin)
# admin.site.register(Passenger, PassengerAdmin)
admin.site.register(Categories)
admin.site.register(Bids,BidsAdmin)
admin.site.register(User,UserDisplay)
admin.site.register(Comments,CommentAdmin)
