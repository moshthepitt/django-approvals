"""Views module for model reviews."""
from django.views import View
from django.views.generic import DetailView, FormView
from django.views.generic.detail import SingleObjectMixin

from model_reviews.forms import get_review_form
from model_reviews.models import ModelReview


class ReviewFormMixin:  # pylint: disable=too-few-public-methods
    """Mixin that implements a method to get review form."""

    model = ModelReview
    template_name = "model_reviews/modelreview_detail.html"

    def get_form_class(self):
        """Return the form class to use."""
        return get_review_form(review=self.get_object(), user=self.request.user)


class ReviewDisplay(ReviewFormMixin, DetailView):
    """Detailview for a model review object."""

    def get_context_data(self, **kwargs):
        """Get context data."""
        context = super().get_context_data(**kwargs)
        form_class = self.get_form_class()
        context["form"] = form_class()
        return context


class ReviewForm(ReviewFormMixin, SingleObjectMixin, FormView):
    """FormView for a review."""

    def get_success_url(self):
        """Get the success url."""
        return "/"

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        form.save()
        return super().form_valid(form)


class ReviewView(View):
    """
    View used to display details of a ModelReview object.

    This view shows both the model review object details as well as handles the
    form to perform a review.

    The structure is inspired by:
        https://docs.djangoproject.com/en/3.0/topics/class-based-views/mixins/#an-alternative-better-solution
    """

    def get(self, request, *args, **kwargs):
        """Get the ReviewDisplay view."""
        view = ReviewDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Get the ReviewForm view."""
        view = ReviewForm.as_view()
        return view(request, *args, **kwargs)
