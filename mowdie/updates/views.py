from django.contrib import messages
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.datetime_safe import datetime
from django.views.generic import View, RedirectView, ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Update, Favorite
from .forms import UpdateForm


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args,
                                                        **kwargs)


class UpdateRedirectView(RedirectView):
    permanent = True

    def get_redirect_url(self, update_id):
        return "/updates/{}".format(update_id)


class UpdateListView(ListView):
    template_name = "updates/update_list.html"
    model = Update
    context_object_name = 'updates'
    queryset = Update.objects.order_by('-posted_at').annotate(
        Count('favorite')).select_related()
    paginate_by = 20
    header = "All updates"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = self.header
        if self.request.user.is_authenticated():
            favorites = self.request.user.favorited_updates.all()
        else:
            favorites = []
        context["favorites"] = favorites
        return context


class FollowedUpdatesView(LoginRequiredMixin, UpdateListView):
    header = "Updates from users you follow"

    def get_queryset(self):
        return Update.objects.filter(
            user__profile__followers__user=self.request.user).order_by(
            '-posted_at')


class PopularUpdatesView(UpdateListView):
    header = "Popular updates"
    queryset = Update.objects.annotate(Count('favorite')).order_by(
        '-favorite__count')[:20]


class AddUpdateView(LoginRequiredMixin, View):
    def get(self, request):
        form = UpdateForm()
        return render(request, "updates/add.html", {"form": form})

    def post(self, request):
        form = UpdateForm(request.POST)
        if form.is_valid():
            update = form.save(commit=False)
            update.user = request.user
            update.posted_at = datetime.now()
            update.save()
            messages.add_message(request, messages.SUCCESS,
                                 "Your update was successfully posted!")
            return redirect("index")
        else:
            return render(request, "updates/add.html", {"form": form})


class UpdateView(View):
    def get(self, request, update_id):
        update = get_object_or_404(Update, pk=update_id)
        update.favorite__count = update.favorite_set.count()
        if request.user.is_authenticated():
            favorites = request.user.favorited_updates.all()
        else:
            favorites = []
        return render(request,
                      "updates/update.html",
                      {"update": update,
                       "favorites": favorites})


@login_required
def add_favorite(request, update_id):
    update = get_object_or_404(Update, pk=update_id)
    if request.user not in update.favorited_users.all():
        update.favorite_set.create(user=request.user)
        messages.add_message(request, messages.SUCCESS,
                             "You have favorited this update.")
    return redirect("show_update", update.id)


@login_required
def delete_favorite(request, update_id):
    update = get_object_or_404(Update, pk=update_id)
    try:
        favorite = update.favorite_set.get(user=request.user)
        favorite.delete()
        messages.add_message(request, messages.SUCCESS,
                             "You have unfavorited this update.")
    except Favorite.DoesNotExist:
        messages.add_message(request, messages.ERROR,
                             "This was not a favorite update.")

    return redirect("show_update", update.id)
