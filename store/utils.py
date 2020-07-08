import random
import string

from django.utils.text import slugify

#generates a random numbers based on the given size, with a default of 110
def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):

    return ''.join(random.choice(chars) for _ in range(size))

# the function assumes that your instance is a model which contains a slug and title
def unique_slug_generator(instance, new_slug=None):

    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = '{slug}-{randstr}'.format(
            slug=slug,
            randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug