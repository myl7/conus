from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.urls import reverse_lazy

from . import forms
from .models import Notice
from .tasks.email import notify_email


class NoticeCreateView(PermissionRequiredMixin, CreateView):
    form_class = forms.NoticeCreateForm
    template_name = 'notice/notice_create.html'
    permission_required = 'notice.add_notice'
    success_url = reverse_lazy('notice:list_send')

    def form_valid(self, form):
        form.instance.from_user = self.request.user
        res = super().form_valid(form)
        notify_email.delay([
            (user.contactinfo.email, user.first_name) for user in form.instance.to_users.all()
        ], form.instance.title, form.instance.body)
        return res


class NoticeSendListView(PermissionRequiredMixin, ListView):
    permission_required = 'notice.add_notice'
    template_name = 'notice/notice_send_list.html'

    def get_queryset(self):
        return Notice.objects.filter(from_user=self.request.user)


class NoticeRecvListView(LoginRequiredMixin, ListView):
    template_name = 'notice/notice_recv_list.html'

    def get_queryset(self):
        return Notice.objects.filter(to_users=self.request.user)
