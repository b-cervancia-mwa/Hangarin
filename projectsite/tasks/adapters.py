from django.contrib.auth import get_user_model
from django.utils.text import slugify

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class HangarinSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        user_model = get_user_model()
        username_field = getattr(user_model, 'USERNAME_FIELD', 'username')
        current_username = getattr(user, username_field, '')

        if current_username:
            return user

        base_username = (
            data.get('username')
            or (data.get('email') or '').split('@')[0]
            or slugify(data.get('name', '')).replace('-', '')
            or sociallogin.account.provider
        )
        base_username = slugify(base_username).replace('-', '')[:24] or 'hangarinuser'
        candidate = base_username
        suffix = 1

        while user_model.objects.filter(**{username_field: candidate}).exists():
            candidate = f'{base_username[:20]}{suffix}'
            suffix += 1

        setattr(user, username_field, candidate)
        return user
