from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):

    def create_user(self, username, email, password, **kwargs):
        if not username or not email:
            raise ValueError('Укажите username и email')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password, **kwargs):
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_staff', True)

        if kwargs.get('is_staff') is not True:
            raise ValueError('Superuser должен иметь is_staff=True')
        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser должен иметь is_superuser=True')
        return self.create_user(username, email, password, **kwargs)
