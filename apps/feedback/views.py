from django.contrib import messages
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView

from apps.feedback.forms import CreateFeedBackForm
from apps.feedback.models import Recaptcha

from common.utils import get_random_model

CAPTCHA_SESSION_KEY = 'feedback_captcha_id'


class ContactsView(FormView):
    form_class = CreateFeedBackForm
    template_name = 'contacts.html'

    def get_captcha(self):
        """Капча, которую пользователь видел на странице (id хранится в сессии)."""
        captcha_id = self.request.session.get(CAPTCHA_SESSION_KEY)
        if captcha_id is None:
            return None
        return Recaptcha.objects.filter(pk=captcha_id).first()

    def rotate_captcha(self, exclude=None):
        """Показываем новую капчу: одну картинку нельзя перебирать несколькими попытками."""
        captcha = get_random_model(Recaptcha, exclude_pk=exclude.pk if exclude else None)
        if captcha:
            self.request.session[CAPTCHA_SESSION_KEY] = captcha.pk
        else:
            self.request.session.pop(CAPTCHA_SESSION_KEY, None)
        return captcha

    def get(self, request, *args, **kwargs):
        self.captcha = self.rotate_captcha()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.captcha = self.get_captcha()
        return super().post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['captcha'] = self.captcha
        # Капча нужна, только если в базе есть хотя бы одна
        kwargs['captcha_required'] = Recaptcha.objects.exists()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recaptcha'] = self.captcha
        return context

    def form_valid(self, form):
        form.save()
        self.rotate_captcha(exclude=self.captcha)
        messages.success(self.request, _('Спасибо! Ваше сообщение отправлено.'))
        return super().form_valid(form)

    def form_invalid(self, form):
        # После неудачной попытки — новая картинка
        self.captcha = self.rotate_captcha(exclude=self.captcha)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('contacts') + '#feedback'
