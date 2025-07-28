from django.core.exceptions import ValidationError
from django.db import models
from django.urls import NoReverseMatch, reverse


class Menu(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='items')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=200, blank=True, null=True)
    named_url = models.CharField(max_length=100, blank=True, null=True)
    parent = models.ForeignKey(
    'self', 
    on_delete=models.CASCADE, 
    null=True, 
    blank=True, 
    related_name='children'
)

    class Meta:
        ordering = ['id']  # to preserve ordering

    def get_absolute_url(self):
        if self.named_url:
            try:
                return reverse(self.named_url)
            except NoReverseMatch:
                return '#'
        return self.url or '#'

    def clean(self):
        if not self.url and not self.named_url:
            raise ValidationError("Either 'url' or 'named_url' must be specified.")
        if self.url and self.named_url:
            raise ValidationError("Only one of 'url' or 'named_url' should be specified.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
