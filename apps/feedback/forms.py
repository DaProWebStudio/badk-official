from django.core.exceptions import ValidationError
from django.forms import ModelForm, Textarea, TextInput, EmailInput, IntegerField, NumberInput
from django.utils.translation import gettext_lazy as _

from .models import FeedBack

# Tailwind-классы полей формы (шаблон contacts.html)
INPUT_CLASS = (
    'h-12 w-full rounded-2xl border border-line bg-white px-4 text-[15px] text-ink outline-none transition '
    'placeholder:text-muted/60 focus:border-gold focus:ring-4 focus:ring-gold/15 '
    'aria-invalid:border-red-500 aria-invalid:ring-red-500/15'
)
TEXTAREA_CLASS = INPUT_CLASS.replace('h-12', 'min-h-40 py-3 leading-relaxed')


class CreateFeedBackForm(ModelForm):
    user_answer = IntegerField(widget=NumberInput(attrs={'class': INPUT_CLASS, 'placeholder': _('Напишите ответ')}))

    def __init__(self, *args, captcha=None, captcha_required=True, **kwargs):
        self.captcha = captcha
        super().__init__(*args, **kwargs)
        if not captcha_required:
            del self.fields['user_answer']
        for visible in self.visible_fields():
            visible.field.widget.attrs['required'] = 'required'

    def clean_user_answer(self):
        answer = self.cleaned_data['user_answer']
        # Нет капчи в сессии — сессия истекла или форму отправили не со страницы
        if self.captcha is None or answer != self.captcha.answer:
            raise ValidationError(_('Не правильный ответ'))
        return answer

    class Meta:
        model = FeedBack
        fields = ['name', 'email', 'message', 'user_answer']
        widgets = {
            'name': TextInput(attrs={
                'class': INPUT_CLASS,
                "placeholder": _("Ваше имя"),
                "minlength": "3",
                "maxlength": "25",
            }),
            'email': EmailInput(attrs={
                'class': INPUT_CLASS,
                "placeholder": _("Ваша электронная почта"),
            }),
            'message': Textarea(attrs={
                'class': TEXTAREA_CLASS,
                "placeholder": _("Ваше сообщение"),
                "minlength": "20",
                "maxlength": "5000",
            }),
        }
