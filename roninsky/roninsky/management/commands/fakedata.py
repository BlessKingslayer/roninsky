from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from random import choice, randint
from django.contrib.auth.models import User
from factory import Faker as FacFaker, fuzzy
from factory.django import DjangoModelFactory

from blog.models import Category, Tag, Post


def fake_category():
    fake = Faker('zh_CN')
    name = fake.word()
    is_nav = fake.pybool()
    owner = choice(User.objects.all())
    # created_time = choice([fake.date_object() for _ in range(20)])

    from django.db import transaction
    try:
        with transaction.atomic():
            Category.objects.create(
                name=name, is_nav=is_nav, owner=owner
            )
    except Exception as e:
        print(str(e), ', name = %s' % name)


def fake_tag():
    class TagFactory(DjangoModelFactory):
        class Meta:
            model = Tag

        name = FacFaker('word', locale='zh_CN')
        owner = fuzzy.FuzzyChoice(User.objects.all())

    from django.db import transaction
    try:
        with transaction.atomic():
            TagFactory()
    except Exception as e:
        print(str(e))


def fake_post():
    fake = Faker('zh_CN')
    title = fake.sentence(
        nb_words=4, variable_nb_words=True,
        ext_word_list=None)[:-1]
    desc = fake.paragraph(
        nb_sentences=5, variable_nb_sentences=True,
        ext_word_list=None)
    content = fake.text(max_nb_chars=800, ext_word_list=None)
    randNum = randint(0, Category.objects.count() - 1)
    category = Category.objects.all()[randNum]
    randNum = randint(0, Tag.objects.count() - 1)
    tag = Tag.objects.all()[randNum]
    owner = choice(User.objects.all())

    from django.db import transaction
    try:
        with transaction.atomic():
            Post.objects.create(
                title=title, desc=desc, content=content, category=category,
                tag=tag, owner=owner
            )
    except Exception as e:
        print(str(e), ', title = %s' % title)


class Command(BaseCommand):
    help = '生成虚拟的测试数据'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count', default=10,
            type=int, help='创建虚拟数据的数量.')

        parser.add_argument('kind', type=str, default='all')

    def handle(self, *args, **options):
        # user = authenticate(username='wangjiawei', password='wangjiawei')

        def do_all():
            fake_category()
            fake_tag()
            fake_post()

        do_fake_data = {
            'all': do_all,
            'category': fake_category,
            'tag': fake_tag,
            'post': fake_post,
        }

        self.stdout.write(self.style.SUCCESS('begin import'))
        for _ in range(options['count']):
            do_fake_data[options['kind']]()
        self.stdout.write(self.style.SUCCESS('end import'))
