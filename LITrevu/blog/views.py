from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Ticket, Review
from .forms import TicketForm, ReviewForm
from itertools import chain
from operator import attrgetter


@login_required
def home(request):
    tickets = Ticket.objects.all()
    reviews = Review.objects.all()
    combined_list = sorted(
        chain(tickets, reviews),
        key=lambda instance: instance.time_created,
        reverse=True
    )

    # Ajout d'une clé 'type' pour chaque élément dans la liste
    for item in combined_list:
        item.item_type = 'ticket' if isinstance(item, Ticket) else 'review'
    
    return render(request, 'blog/home.html', context={'combined_list': combined_list})

@login_required
def create_ticket(request):
    if request.method =='POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TicketForm()
    return render(request, 'blog/create_ticket.html', context={'form':form} )

@login_required
def update_ticket(request, ticket_id):  
    ticket = Ticket.objects.get(id=ticket_id)
    if request.method =='POST':
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TicketForm(instance=ticket)
    return render ( request, 'blog/update_ticket.html', context={'form':form})

@login_required
def delete_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    if request.method =='POST':
        ticket.delete()
        return redirect('home')
    return render(request, 'blog/delete_ticket.html', context={'ticket':ticket})

@login_required
def create_review(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    if request.method =='POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect('home')
    else:
        form = ReviewForm()
    return render (request, 'blog/create_review.html', context={'form':form, 'ticket':ticket})

@login_required
def update_review(request, review_id):
    review = Review.objects.get(id=review_id)
    if request.method =='POST':
        form = ReviewForm(request.POST, request.FILES, instance=review)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ReviewForm(instance=review)
    return render ( request, 'blog/update_review.html', context={'form':form})

@login_required
def delete_review(request, review_id):
    review = Review.objects.get(id=review_id)
    if request.method =='POST':
        review.delete()
        return redirect('home')
    return render(request, 'blog/delete_review.html', context={'review':review})


@login_required
def create_ticket_and_review(request):
    if request.method == 'POST':
        form_ticket = TicketForm(request.POST, request.FILES)
        form_review = ReviewForm(request.POST)
        
        if form_ticket.is_valid() and form_review.is_valid():
            # On sauvegarde d'abord le ticket
            ticket = form_ticket.save(commit=False)
            ticket.save()
            
            # Ensuite, on lie la critique au ticket et on la sauvegarde
            review = form_review.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            
            return redirect('home')
    else:
        form_ticket = TicketForm()
        form_review = ReviewForm()
    
    return render(request, 'blog/create_ticket_and_review.html', context={
        'form_ticket': form_ticket,
        'form_review': form_review
    })


@login_required
def user_reviews(request):
    reviews = Review.objects.filter(user=request.user)
    return render(request, 'blog/user_reviews.html', {'reviews': reviews})