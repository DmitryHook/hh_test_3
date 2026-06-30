import random
from datetime import date, timedelta

from django.core.management.base import BaseCommand

from dds.models import (
    Category,
    Status,
    SubCategory,
    Transaction,
    TransactionType
)


class Command(BaseCommand):
    help = "Заполняет базу данных начальными справочниками и тестовыми транзакциями"

    def add_arguments(self, parser):
        parser.add_argument(
            "count",
            nargs="?",
            type=int,
            default=50,
            help="Количество тестовых транзакций",
        )

    def handle(self, *args, **options):
        self.stdout.write("Начало инициализации данных")

        count = options["count"]

        for status_name in ["Бизнес", "Личное", "Налог"]:
            Status.objects.get_or_create(name=status_name)

        type_income, _ = TransactionType.objects.get_or_create(name="Пополнение")
        type_outcome, _ = TransactionType.objects.get_or_create(name="Списание")

        categories_data = {
            "Инфраструктура": (type_outcome, ["VPS", "Proxy"]),
            "Маркетинг": (type_income, ["Farpost", "Avito"]),
        }

        for category_name, (transaction_type, subcategories) in categories_data.items():
            category, _ = Category.objects.get_or_create(
                name=category_name, transaction_type=transaction_type
            )
            for subcategory_name in subcategories:
                SubCategory.objects.get_or_create(
                    name=subcategory_name, category=category
                )

        if Transaction.objects.count() == 0:
            self.stdout.write("Генерация тестовых транзакций")

            all_statuses = list(Status.objects.all())
            all_subcategories = list(
                SubCategory.objects.select_related("category__transaction_type")
            )
            today = date.today()

            transactions_to_create = []
            for _ in range(count):
                random_subcategory = random.choice(all_subcategories)
                random_status = random.choice(all_statuses)
                random_days_offset = random.randint(0, 180)
                random_amount = round(random.uniform(500, 50000), 2)

                comment_text = "Тестовая запись" if random.random() > 0.5 else ""

                transactions_to_create.append(
                    Transaction(
                        date=today - timedelta(days=random_days_offset),
                        status=random_status,
                        transaction_type=random_subcategory.category.transaction_type,
                        category=random_subcategory.category,
                        subcategory=random_subcategory,
                        amount=random_amount,
                        comment=comment_text,
                    )
                )

            Transaction.objects.bulk_create(transactions_to_create)
            self.stdout.write(self.style.SUCCESS("Тестовые транзакции созданы."))
        else:
            self.stdout.write(
                self.style.WARNING("Транзакции уже существуют, генерация пропущена.")
            )

        self.stdout.write(self.style.SUCCESS("Данные успешно загружены!"))
