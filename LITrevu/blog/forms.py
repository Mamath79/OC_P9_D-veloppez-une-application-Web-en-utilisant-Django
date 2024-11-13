from django import forms
from django.contrib.auth import get_user_model
from .models import Ticket, Review, UserFollows


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["headline", "body", "rating"]
        labels = {
            "headline": "Titre",
            "body": "Commentaire",
            "rating": "Note",
        }


User = get_user_model()


class FollowUsersForm(forms.ModelForm):
    class Meta:
        model = UserFollows
        fields = ["followed_user"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            # Limiter le choix aux utilisateurs non suivis
            self.fields["followed_user"].queryset = User.objects.exclude(
                id__in=user.following.values_list("followed_user", flat=True)
            ).exclude(id=user.id)
