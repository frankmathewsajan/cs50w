from auctions.models import Listing, Category

def active_listings(request):
    return {'active_listings': Listing.objects.filter(status=True)}

def all_categories(request):
    return {'all_categories': Category.objects.all()}
