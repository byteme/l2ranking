from django.views import generic as generic_views
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib import messages

from usercp import forms as usercp_forms


class Register(generic_views.CreateView):
    """
    User registration view.
    """

    template_name = 'usercp/register.html'
    form_class = usercp_forms.RegisterForm

    def get_success_url(self):
        return reverse('usercp:login')


class AccountUpdate(generic_views.UpdateView):
    """
    User account update view.
    """

    model = User
    template_name = 'usercp/account.html'
    form_class = usercp_forms.AccountUpdateForm

    def get_success_url(self):
        if self.request.POST:
            messages.success(self.request, 'Account information successfully updated.')
        return reverse('usercp:account')

    def get_object(self, queryset=None):
        return self.request.user
