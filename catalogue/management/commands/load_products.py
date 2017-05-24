from random import choice, randint

from django.core.management.base import BaseCommand, CommandError

from catalogue.models import Product, Category


class Command(BaseCommand):
    help = 'create product catalogue from file'

    def __init__(self):
        super(Command, self).__init__()
        self.categories = Category.objects.all()

    def add_arguments(self, parser):
        parser.add_argument('file_name', nargs='+', type=str)

    def handle(self, *args, **options):
        for filename in options['file_name']:
            try:
                with open(filename) as file:
                    for product in file:
                        Product.objects.create(name=product,
                                               product_category=choice(
                                                   self.categories),
                                               description='description',
                                               price=randint(1, 999999),
                                               num_in_stock=randint(1, 999999))
                        self.stdout.write(self.style.SUCCESS(
                            'Successfully created "%s"' % product))
            except IOError as e:
                raise CommandError(
                    'file {} does not exists'.format(['file_name']))

        self.stdout.write(self.style.SUCCESS('DONE!'))
