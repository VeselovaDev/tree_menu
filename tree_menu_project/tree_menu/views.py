from django.views.generic import TemplateView

from tree_menu.models import Menu


class BaseMenuView(TemplateView):
    # Inject the first available menu into all templates using this base view
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu"] = Menu.objects.first()
        return context


class HomeView(BaseMenuView):
    template_name = "home.html"


class AboutView(BaseMenuView):
    template_name = "about.html"


class TeamView(BaseMenuView):
    template_name = "team.html"


class ContactView(BaseMenuView):
    template_name = "contact.html"


class ParentView(BaseMenuView):
    template_name = 'parent.html'

class ParentChildView(BaseMenuView):
    template_name = 'parent_child.html'