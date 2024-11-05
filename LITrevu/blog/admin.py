from django.contrib import admin
from .models import Ticket, Review, UserFollows

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'time_created', 'image')
    search_fields = ('title', 'description')
    list_filter = ('time_created',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('headline', 'rating', 'user', 'time_created')
    search_fields = ('headline', 'body')
    list_filter = ('rating', 'time_created')

@admin.register(UserFollows)
class UserFollowsAdmin(admin.ModelAdmin):
    list_display = ('user', 'followed_user')
    search_fields = ('user__username', 'followed_user__username')
