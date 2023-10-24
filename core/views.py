import datetime
from django.views.generic.detail import DetailView
from django.views.generic import ListView, TemplateView
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Subscriber, Category, ESTADO_CHOICES


class TableView(ListView):
    def get_ordering(self):
        current_date = datetime.datetime.now()
        day_of_week = current_date.weekday()
        choices = [
            "company__id",
            "-id",
            "company__tel1",
            "company__document",
            "-company__id",
            "-company__tel1",
            "-company__document",
        ]

        return choices[day_of_week]


class HomeView(TemplateView):
    template_name = "pages/index.html"


class SubscribersListView(TableView):
    model = Subscriber
    template_name = "pages/list.html"
    context_object_name = "subs"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        actives = queryset.filter(active=True)
        return actives

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["estados"] = ESTADO_CHOICES
        context["categories"] = Category.objects.all()

        return context


class SubscriberSearchView(TableView):
    model = Subscriber
    template_name = "pages/search.html"
    context_object_name = "subs"
    paginate_by = 10
    ordering = "company__name"

    def get_queryset(self):
        queryset = super().get_queryset()
        actives = queryset.filter(active=True)
        search_term = self.request.GET.get("search_term")
        ctg_pk = self.request.GET.get("category")
        q = search_term if bool(search_term) else ""
        uf = self.request.GET.get("location")

        if uf == "n":
            if ctg_pk == "t":
                qs = actives.filter(Q(company__name__icontains=q))
                return qs
            qs = actives.filter(
                Q(
                    Q(company__name__icontains=q)
                    & Q(company__categoria1=ctg_pk)
                )
                | Q(
                    Q(company__name__icontains=q)
                    & Q(company__categoria2=ctg_pk)
                )
            )
            return qs
        else:
            if ctg_pk == "t":
                qs = actives.filter(
                    Q(company__name__icontains=q) & Q(company__uf=uf)
                )
                return qs
            qs = actives.filter(
                Q(
                    Q(company__name__icontains=q)
                    & Q(company__categoria1=ctg_pk)
                    & Q(company__uf=uf)
                )
                | Q(
                    Q(company__name__icontains=q)
                    & Q(company__categoria2=ctg_pk)
                    & Q(company__uf=uf)
                )
            )
            return qs

    def get_context_data(self, **kwargs):
        search_term = self.request.GET.get("search_term")
        q = search_term if bool(search_term) else ""
        c = self.request.GET.get("category")
        uf = self.request.GET.get("location")
        context = super().get_context_data(**kwargs)
        context["l"] = uf
        context["s"] = q
        context["c"] = c
        context["estados"] = ESTADO_CHOICES
        context["categories"] = Category.objects.all()
        return context


class SubscriberDetailView(DetailView):
    model = Subscriber
    template_name = "pages/details.html"

    def get_object(self, queryset=None):
        username = self.kwargs.get("username")

        return get_object_or_404(Subscriber, username=username, active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sub"] = self.get_object()
        return context


class AboutView(TemplateView):
    template_name = "pages/about.html"
