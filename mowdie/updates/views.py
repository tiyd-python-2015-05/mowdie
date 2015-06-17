from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.db.models import Count
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.datetime_safe import datetime
from django.views.generic import View, RedirectView, ListView, CreateView, \
    DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Update, Favorite
from .forms import UpdateForm


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class UpdateRedirectView(RedirectView):
    permanent = True

    def get_redirect_url(self, update_id):
        return "/updates/{}".format(update_id)


class UpdateListView(ListView):
    model = Update
    context_object_name = 'updates'
    template_name = "updates/update_list.html"
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
            '-posted_at').annotate(
            Count('favorite')).select_related()


class PopularUpdatesView(UpdateListView):
    header = "Popular updates"
    queryset = Update.objects.annotate(Count('favorite')).order_by(
        '-favorite__count').annotate(
        Count('favorite')).select_related()[:20]


class UpdateCreate(LoginRequiredMixin, CreateView):
    model = Update
    fields = ['text']

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.posted_at = timezone.now()
        messages.add_message(self.request, messages.SUCCESS,
                             "Your update was successfully posted!")
        return super().form_valid(form)


class UpdateDelete(LoginRequiredMixin, DeleteView):
    model = Update
    success_url = reverse_lazy('index')

    def get_queryset(self):
        return Update.objects.filter(user=self.request.user)


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


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib
matplotlib.style.use('ggplot')

def updates_chart(request):
    updates = Update.objects.all()
    df = pd.DataFrame(model_to_dict(update) for update in updates)
    df['count'] = 1
    df.index = df['posted_at']
    counts = df['count']
    counts = counts.sort_index()
    series = pd.expanding_count(counts).resample('W', how=np.max, fill_method='pad')
    response = HttpResponse(content_type='image/png')

    fig = plt.figure()
    # ax = fig.add_subplot(111)
    # ax.plot(series)
    series.plot()
    plt.title("Total updates over time")
    plt.xlabel("")
    canvas = FigureCanvas(fig)
    canvas.print_png(response)
    return response
