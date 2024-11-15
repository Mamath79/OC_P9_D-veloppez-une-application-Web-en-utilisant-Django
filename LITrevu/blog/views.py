from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from .models import Ticket, Review, UserFollows
from .forms import TicketForm, ReviewForm, FollowUsersForm
from itertools import chain
from django.shortcuts import get_object_or_404


@login_required
def home(request):
    followed_users = request.user.following.values_list(
        "followed_user", flat=True
    )
    tickets = Ticket.objects.filter(
        user__in=followed_users
    ) | Ticket.objects.filter(user=request.user)
    reviews = Review.objects.filter(
        user__in=followed_users
    ) | Review.objects.filter(user=request.user)

    combined_list = sorted(
        chain(tickets, reviews),
        key=lambda instance: instance.time_created,
        reverse=True,
    )

    # Ajouter un indicateur si la liste est vide
    is_empty = not combined_list

    for item in combined_list:
        item.item_type = "ticket" if isinstance(item, Ticket) else "review"
        if isinstance(item, Review):
            item.filled_stars = range(item.rating)
            item.empty_stars = range(5 - item.rating)

    return render(
        request,
        "blog/flux.html",
        context={
            "combined_list": combined_list,
            "followed_users": followed_users,
            "is_empty": is_empty,
        },
    )


@login_required
@permission_required("blog.add_ticket", raise_exception=True)
def create_ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect("flux")
    else:
        form = TicketForm()
    return render(request, "blog/create_ticket.html", context={"form": form})


@login_required
@permission_required("blog.change_ticket", raise_exception=True)
def update_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    if ticket.user != request.user:
        return redirect("permission_denied")
    if ticket.user != request.user:
        return redirect("flux")
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect("flux")
    else:
        form = TicketForm(instance=ticket)
    return render(request, "blog/update_ticket.html", context={"form": form})


@login_required
@permission_required("blog.delete_ticket", raise_exception=True)
def delete_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    if ticket.user != request.user:
        return redirect("permission_denied")
    if request.method == "POST":
        ticket.delete()
        return redirect("flux")
    return render(
        request, "blog/delete_ticket.html", context={"ticket": ticket}
    )


@login_required
@permission_required("blog.add_review", raise_exception=True)
def create_review(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    # Vérifie si l'utilisateur a déjà publié une critique pour ce billet
    if Review.objects.filter(ticket=ticket, user=request.user).exists():
        return redirect("permission_denied")

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect("flux")
    else:
        form = ReviewForm()
    return render(
        request,
        "blog/create_review.html",
        context={"form": form, "ticket": ticket},
    )


@login_required
@permission_required("blog.change_review", raise_exception=True)
def update_review(request, review_id):
    review = Review.objects.get(id=review_id)
    if review.user != request.user:
        return redirect("permission_denied")
    if request.method == "POST":
        form = ReviewForm(request.POST, request.FILES, instance=review)
        if form.is_valid():
            form.save()
            return redirect("flux")
    else:
        form = ReviewForm(instance=review)
    return render(request, "blog/update_review.html", context={"form": form})


@login_required
@permission_required("blog.delete_review", raise_exception=True)
def delete_review(request, review_id):
    review = Review.objects.get(id=review_id)
    if review.user != request.user:
        return redirect("permission_denied")
    if request.method == "POST":
        review.delete()
        return redirect("flux")
    return render(
        request, "blog/delete_review.html", context={"review": review}
    )


@login_required
@permission_required("blog.add_ticket", raise_exception=True)
@permission_required("blog.add_review", raise_exception=True)
def create_ticket_and_review(request):
    if request.method == "POST":
        form_ticket = TicketForm(request.POST, request.FILES)
        form_review = ReviewForm(request.POST)

        if form_ticket.is_valid() and form_review.is_valid():
            # On sauvegarde d'abord le ticket
            ticket = form_ticket.save(commit=False)
            ticket.user = request.user
            ticket.save()

            # Ensuite, on lie la critique au ticket et on la sauvegarde
            review = form_review.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()

            return redirect("flux")
    else:
        form_ticket = TicketForm()
        form_review = ReviewForm()

    return render(
        request,
        "blog/create_ticket_and_review.html",
        context={"form_ticket": form_ticket, "form_review": form_review},
    )


@login_required
def user_reviews(request):
    reviews = Review.objects.filter(user=request.user)
    return render(request, "blog/user_reviews.html", {"reviews": reviews})


@login_required
def user_posts(request):
    user_tickets = Ticket.objects.filter(user=request.user)
    user_reviews = Review.objects.filter(user=request.user)

    combined_list = sorted(
        chain(user_tickets, user_reviews),
        key=lambda instance: instance.time_created,
        reverse=True,
    )

    # Ajouter un indicateur si la liste est vide
    is_empty = not combined_list

    for item in combined_list:
        item.item_type = "ticket" if isinstance(item, Ticket) else "review"
        if isinstance(item, Review):
            item.filled_stars = range(item.rating)
            item.empty_stars = range(5 - item.rating)

    return render(
        request,
        "blog/user_posts.html",
        context={
            "combined_list": combined_list,
            "is_empty": is_empty,
        },
    )


@login_required
def follow_users(request):
    form = FollowUsersForm(user=request.user)
    user_followings = UserFollows.objects.filter(user=request.user)
    user_followers = UserFollows.objects.filter(
        followed_user=request.user
    )  # Liste des abonnés

    if request.method == "POST":
        form = FollowUsersForm(request.POST, user=request.user)
        if form.is_valid():
            follow_instance = form.save(commit=False)
            follow_instance.user = request.user
            follow_instance.save()
            return redirect("follow_user")

    return render(
        request,
        "blog/follow_user.html",
        {
            "form": form,
            "user_followings": user_followings,
            "user_followers": user_followers,
        },
    )


@login_required
def delete_followed_user(request, follow_id):
    follow_instance = get_object_or_404(
        UserFollows, id=follow_id, user=request.user
    )

    if request.method == "POST":
        follow_instance.delete()
        return redirect("follow_user")

    # Rendre le template avec le nom de l'utilisateur suivi
    return render(
        request,
        "blog/delete_followed_user.html",
        {"followed_user": follow_instance.followed_user},
    )


def permission_denied_view(request):
    return render(
        request,
        "blog/permission_denied.html",
        {
            "message": "Vous n'avez pas les autorisations nécessaires pour accéder à cette ressource."
        },
    )
