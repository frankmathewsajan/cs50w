from django.contrib import admin
from auctions.models import *
# Register your models here.

admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(Watchlist)
admin.site.register(User)
admin.site.register(Bid)
admin.site.register(Comment)
