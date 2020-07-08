from django.db import models
from django.utils.translation import ugettext_lazy 
from django.conf import settings
from django.urls import reverse
from django.db.models.signals import pre_save
from authentication.models import User

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


    # purchase's header fields
class PurchaseOrder(models.Model):

    timestamp = models.DateTimeField(verbose_name=ugettext_lazy('Timestamp'))
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=ugettext_lazy('User')
    )

    cart = models.BooleanField(verbose_name=ugettext_lazy('Cart'))

    class Meta:

        verbose_name = ugettext_lazy('PurchaseOrder')
        verbose_name_plural = ugettext_lazy('PurchaseOrders')
    
    def __str__(self):
        return 'PurchaseOrder - {}'.format(self.id)

    def __repr__(self):
        return ('PurchaseOrder(id={},timestamp={},user={},cart={})').format(
            self.id,
            self.timestamp,
            self.user,
            self.cart
        )
    
    # The products of a specific PurchaseOrder.
class PurchaseItem(ProductBase):

    id = models.AutoField(primary_key=True)
    
    barcode = models.CharField(
        max_length=20, verbose_name=ugettext_lazy('Barcode')
    )

    purchase_order = models.ForeignKey(
        PurchaseOrder, on_delete=models.CASCADE,
        verbose_name=ugettext_lazy('PurchaseOrder')
    )

    quantity = models.DecimalField(
        max_digits=8, decimal_places=3, verbose_name=ugettext_lazy('Quantity')
    )

    total_price = models.DecimalField(
        max_digits=8, decimal_places=3,
        verbose_name=ugettext_lazy('TotalPrice')
    )

    slug = None  # purchaseItem class doesnt utilize slug.

    class Meta:
        verbose_name = ugettext_lazy('PurchaseItem')
        verbose_name_plural = ugettext_lazy('PurchaseItems')
    
    def __str__(self):
        return 'PurchaseItem {} - order {}'.format(
            self.id, self.purchase_order.id
        )
    
    def __repr__(self):
        return (
            'PurchaseItem(id={},barcode={},purchase_order={},'
            'quantity={},total_price={})'.format(
                self.id,
                self.barcode,
                self.purchase_order.id,
                self.quantity,
                self.total_price
            )
        )

      # the payment methods chosen by the user for specific purchase order
class PurchasePaymentMethod(models.Model):

    purchase_order = models.ForeignKey(
        PurchaseOrder, on_delete=models.CASCADE,
        verbose_name=ugettext_lazy('PurchaseOrder')
    )

    payment_method = models.ForeignKey(
        PaymentMethod, on_delete=models.PROTECT,
        verbose_name=ugettext_lazy('PaymentMethod')
    )

    value = models.DecimalField(
        max_digits=8, decimal_places=3, verbose_name=ugettext_lazy('Value')
    )

    class Meta:

        verbose_name = ugettext_lazy('PurchasePaymentMethod')
        verbose_name_plural = ugettext_lazy('PurchasePaymentMethods')
    
    def __str__(self):
        return 'PurchasePaymentMethod {} - order {}'.format(
            self.id, self.purchase_order.id
        )
    
    def __repr__(self):
        return (
            'PurchasePaymentMethod(id={},purchase_order={},'
            'payment_method={},value={})'.format(
                self.id,
                self.purchase_order.id,
                self.payment_method.description,
                self.value
            )
        )








    
    


    






    



