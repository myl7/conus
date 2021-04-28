from django.views.generic import CreateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy

from . import forms


class NoticeCreateView(PermissionRequiredMixin, CreateView):
    form_class = forms.NoticeCreateForm
    template_name = 'notice/notice_create.html'
    permission_required = 'notice.add_notice'
    success_url = reverse_lazy('user:detail')

    def form_valid(self, form):
        form.instance.from_user = self.request.user
        return super().form_valid(form)
