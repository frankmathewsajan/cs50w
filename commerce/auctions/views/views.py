from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

from auctions.forms import ListingForm
from auctions.models import Listing, Category, Watchlist, Comment, Bid



def index(request):
    listings = Listing.objects.order_by('-status') 
    return render(request, "auctions/index.html", {"listings": listings})

def close(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    highest_bid = listing.bids.order_by('-amount').first()
    winner = highest_bid.user if highest_bid else None
    if request.method == "POST":
        if (request.user == listing.user) and winner:
                listing.status = False
                messages.info(request, f"Listing Closed : {winner} is the highest bidder")
                listing.save()
                return redirect('listings', pk=listing.id) 


def bid(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    highest_bid = listing.bids.order_by('-amount').values_list('amount', flat=True).first() or listing.price
    if request.method == "POST":
        bid = float(request.POST.get('bid'))
        if bid and bid > highest_bid :
            new_bid = Bid(
                user=request.user,
                listing=listing,
                amount=bid)
            new_bid.save()
            listing.price = bid
            listing.save()
        else:
            messages.error(request, f"Let's try that again. Bids must be higher than the current leading bid. ${highest_bid}")
            return redirect("listings", pk=listing.id)
    return redirect("listings", pk=listing.id) 

@login_required
def comment(request, pk):
    listing = get_object_or_404(Listing, pk=pk)

    if request.method == "POST":
        content = request.POST.get('content')
        if content: 
            new_comment = Comment(
                user=request.user,
                listing=listing,
                content=content)
            new_comment.save()

    return redirect("listings", pk=listing.id) 


@login_required
def new(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            new_listing = form.save(commit=False)
            new_listing.user = request.user
            new_listing.save()
            return redirect("listings", pk=new_listing.id)
    else:
        form = ListingForm()
    return render(request, "auctions/new.html", {"form": form})





@login_required
def watchlist(request, pk=0):
    if request.method == "POST":
        listing = get_object_or_404(Listing, pk=pk)

        watchlist_item, created = Watchlist.objects.get_or_create(
            user=request.user, listing=listing
        )
        if not created:
            watchlist_item.delete()
        return redirect("listings", pk=pk)

    watchlist_items = Watchlist.objects.filter(user=request.user).prefetch_related('listing')
    listings = [item.listing for item in watchlist_items]

    return render(request, "auctions/watchlist.html", {"listings": listings})


def listings(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    comments = Comment.objects.filter(listing__id=listing.id).order_by('-created_at') 
    bids = listing.bids.order_by('-amount')

    btn_text_watch = "Watch"
    btn_text_status = "Open Listing"
    color = "primary"
    winner = ''
    
    if not listing.status:
        winner = bids.first().user
    if request.user.is_authenticated:
        btn_text_watch = (
            "Watching"
            if request.user.watchlist.filter(listing_id=listing.id).exists()
            else btn_text_watch
        )
        if listing.status:
            btn_text_status = "Close Listing"
            color = "danger"

    return render(
        request,
        "auctions/listings.html",
        {
            "listing": listing,
            "btn_text_watch": btn_text_watch,
            "toggle_status": request.user == listing.user,
            "btn_text_status": btn_text_status,
            "color": color,
            "comments":comments,
            "bids":bids,
            'winner':winner
        },
    )


def categories(request):
    if request.method == "POST":
        name = request.POST.get("name")
        Category.objects.create(name=name)
        return redirect("categories")

    categories = Category.objects.all()
    return render(
        request,
        "auctions/categories.html",
        {"categories": categories, "url": "category"},
    )


def category(request, pk):
    listings = Listing.objects.filter(category__name=pk)
    return render(
        request, "auctions/category.html", {"category": pk, "listings": listings}
    )
