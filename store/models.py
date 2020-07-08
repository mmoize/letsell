from django.db import models
from django.utils.translation import ugettext_lazy 
from django.conf import settings
from django.urls import reverse
from django.db.models.signals import pre_save

from .utils import unique_slug_generator


# list of categories for the given products
class Category(models.Model):

    
    description = models.CharField(max_length=50, verbose_name=ugettext_lazy('Description'))

    class Meta:

        verbose_name = ugettext_lazy('Category')
        verbose_name_plural = ugettext_lazy('Categories')

    def __str__(self):
        return 'Category - {}'.format(self.description)
    
    def __str__(self):
        return ('Category(description={})').format(self.description)
    
# Productbase Represents both Product and PurchaseItem, it has common fields between the two
class ProductBase(models.Model):

    barcode = models.CharField(primary_key=True, max_length=20, verbose_name=ugettext_lazy('Barcode'))
    title = models.TextField(_(verbose_name=ugettext_lazy('Title'))
    description = models.TextField(verbose_name=ugettext_lazy('Description'))
    image = models.ImageField(verbose_name=ugettext_lazy('Image'), upload_to=None, height_field=None, width_field=None, max_length=None)
    price = models.DecimalField(verbose_name=ugettext_lazy('Price'), max_digits=10, decimal_places=3)
    category = models.ForeignKey(Category, verbose_name=ugettext_lazy('Category'), on_delete=models.CASCADE)

    class Meta:
        abstract = True


    # - The barcode length was chosen considering that usual products come with
    #   EAN-8, EAN-13, UPC-A or UPC-E
    # - The price max length was chosen considering that the most expensive
    #   product in the marketplace is 999.999,999 (using 3 decimal places).
    #   However, this can be changed if needed

class Product(ProductBase):
    
    class Meta:
        verbose_name = ugettext_lazy('Product')
        verbose_name_plural = ugettext_lazy('Products')
    
    barcode = models.CharField(primary_key=True, max_length=20, verbose_name=ugettext_lazy('Barcode'))
    slug = models.SlugField(unique=True)
    
    
    # returns the entire product endpoint(product-details endpoints plus slug field)

    def get_absolute_url(self):
        return reverse('store:product-detail', kwargs={'slug': self.slug})
    
    def __str__(self):
        return 'Product - {}'.format(self.title)

    def __repr__(self):
        return (
            'Product(barcode={},title={},description={},'
            'price={},category={},slug={})'.format(
                self.barcode,
                self.title,
                self.description,
                self.price,
                self.category.description,
                self.slug
            )
        )

    # for slug generation before saving the products instance
def pre_save_product_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(pre_save_product_receiver, sender=Product)

    # different payment methods
class PaymentMethod(models.Model):
    description = models.CharField(unique=True, max_length=50, verbose_name=ugettext_lazy('Description'))

    class Meta:
        verbose_name = ugettext_lazy('PaymentMethod')
        verbose_name_plural = ugettext_lazy('PaymentMethods')

    def __str__(self):
        return 'PaymentMethod - {}'.format(self.description)
    
    def __repr__(self):
        return ('PaymentMethod(description={})').format(self.description)

    
    


    






    



