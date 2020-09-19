from django.db import models
from django.utils.translation import ugettext_lazy 
from django.conf import settings
from django.urls import reverse
from django.db.models.signals import pre_save
from authentication.models import User
from django.http import HttpResponse, JsonResponse
import os


from django_extensions.db.models import (ActivatorModel,TimeStampedModel)
                                         
from djgeojson.fields import PointField
from django.db.models import Q
from django.urls import reverse
from core.models import RandomSlugModel
from authentication.models import User
from django.utils.translation import ugettext_lazy 
from taggit.managers import TaggableManager
from django_resized import ResizedImageField
from django.contrib.gis.db.models import PointField


class Category(models.Model):
    name = models.CharField(max_length=200, default='other')
    slug = models.SlugField(default="other")
    parent = models.ForeignKey('self',blank=True, null=True ,related_name='children', on_delete=models.CASCADE)



    class Meta:
        #enforcing that there can not be two categories under a parent with same slug
        
        # __str__ method elaborated later in post.  use __unicode__ in place of
        
        # __str__ if you are using python 2

        unique_together = ('slug', 'parent',)    
        verbose_name_plural = "categories"     

    def __str__(self):                           
        full_path = [self.name]                  
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])


class Tags(models.Model):
    name = models.CharField(max_length=15, blank=True, )

    def __str__(self):
        template = '{0.name}'
        return template.format(self)

# Productbase Represents both Product and PurchaseItem, it has common fields between the two

class ProductBase(TimeStampedModel):
    barcode = models.CharField(primary_key=True, max_length=20, verbose_name=ugettext_lazy('Barcode'))
    title = models.TextField(verbose_name=ugettext_lazy('Title'))
    description = models.TextField(verbose_name=ugettext_lazy('Description'))
    # image = models.ImageField(verbose_name=ugettext_lazy('Image'), upload_to=None, height_field=None, width_field=None, max_length=None)
    price = models.DecimalField(verbose_name=ugettext_lazy('Price'), max_digits=10, decimal_places=3)
    


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
        ordering = ['-created', '-modified']   
        
    barcode = models.CharField(max_length=20, verbose_name=ugettext_lazy('Barcode'), blank=True)
    slug = models.SlugField(unique=True, blank=True)
    user = models.ForeignKey(User, default=1,  on_delete=models.CASCADE, verbose_name=ugettext_lazy('User'))
    tags = models.ManyToManyField(Tags, related_name='tags', blank=True)
    taggit = TaggableManager(blank=True)
    category = models.ManyToManyField(Category, blank=True)
    

    
    def __str__(self):
        return self.title


    def __repr__(self):
 
        return   ('Productbarcode={},title={},description={},''price={},category={},slug={}').format(
                self.barcode,
                self.title,
                self.description,
                self.price,
                self.category,
                self.slug
            )
        
    def get_cat_list(self):
        k = self.category # for now ignore this instance method
        
        breadcrumb = ["dummy"]
        while k is not None:
            breadcrumb.append(k.slug)
            k = k.parent
        for i in range(len(breadcrumb)-1):
            breadcrumb[i] = '/'.join(breadcrumb[-1:i-1:-1])
        return breadcrumb[-1:0:-1]
        
       

#Product image path for users items/product... not related to the post

def Product_image_path(instance, filename):
    return os.path.join('ProductsImage', str(instance.product.user), filename)

class ProductImage(TimeStampedModel):
    product= models.ForeignKey(Product, on_delete=models.CASCADE)
    image = ResizedImageField(size=[500, 400], upload_to= Product_image_path)
    user = models.ForeignKey(User, default="1", on_delete=models.CASCADE)



    def __str__(self):
        template = '{0.user.username} {0.product.id}'
        return template.format(self)

    class Meta:
        ordering = ['-created',]


#Class holding user post/listing

class Post(models.Model):
    owner = models.ForeignKey(User,  on_delete=models.CASCADE, verbose_name=ugettext_lazy('Owner'))
    location = PointField(null=True, geography=True, blank=True, srid=4326, verbose_name='Location')
    product = models.ManyToManyField(Product, verbose_name=ugettext_lazy("Product"), blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    viewcount = models.IntegerField(default=0)

    class Meta:
        verbose_name = ugettext_lazy('Post')
        verbose_name_plural = ugettext_lazy('Posts')
        ordering = ['-created_at', '-updated_at']  

    def __str__(self):
        template = '{0.owner.username} '
        return template.format(self)


#class holding the number of views per users_listing
class ViewsNumber(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    numberview = models.IntegerField(default=0)
    user = models.ManyToManyField(User, blank=True)





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
class PurchaseOrder(TimeStampedModel):

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








    