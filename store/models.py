from django.db import models
from django.utils.translation import ugettext_lazy 
from django.conf import settings
from django.urls import reverse
from django.db.models.signals import pre_save

from .utils import unique_slug_generator


class Category(models.Model):
    # list of categories for the given products
    
    description = models.CharField(max_length=50, verbose_name=ugettext_lazy('Description'))

    class Meta:

        verbose_name = ugettext_lazy('Category')
        verbose_name_plural = ugettext_lazy('Categories')

    def __str__(self):
        return 'Category - {}'.format(self.description)
    
    def __str__(self):
        return ('Category(description={})').format(self.description)
    

    



