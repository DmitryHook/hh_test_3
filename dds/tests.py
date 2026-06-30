from datetime import date
from decimal import Decimal

from django.test import Client, TestCase
from django.urls import reverse

from .forms import TransactionForm
from .models import Category, Status, SubCategory, Transaction, TransactionType


class TransactionAppTests(TestCase):
    def setUp(self):
        self.client = Client()

        self.status = Status.objects.create(name="Оплачено")
        self.type_expense = TransactionType.objects.create(name="Расход")
        self.category = Category.objects.create(
            name="Продукты", transaction_type=self.type_expense
        )
        self.subcategory = SubCategory.objects.create(
            name="Хлеб", category=self.category
        )

        self.transaction = Transaction.objects.create(
            date=date.today(),
            status=self.status,
            transaction_type=self.type_expense,
            category=self.category,
            subcategory=self.subcategory,
            amount=150.00,
            comment="Тестовый расход",
        )


    def test_transaction_list_view(self):
        """Проверяем главную страницу со списком транзакций"""
        response = self.client.get(reverse("transaction_list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.transaction, response.context["transactions"])


    def test_transaction_create_view_post(self):
        """Проверяем создание новой транзакции через POST-запрос"""
        data = {
            "date": "2026-06-29",
            "status": self.status.id,
            "transaction_type": self.type_expense.id,
            "category": self.category.id,
            "subcategory": self.subcategory.id,
            "amount": "500.00",
            "comment": "Новая транзакция",
        }
        response = self.client.post(reverse("transaction_create"), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Transaction.objects.filter(comment="Новая транзакция").exists())


    def test_transaction_edit_view_post(self):
        """Проверяем редактирование существующей транзакции"""
        url = reverse("transaction_edit", kwargs={"pk": self.transaction.pk})
        data = {
            "date": self.transaction.date,
            "status": self.status.id,
            "transaction_type": self.type_expense.id,
            "category": self.category.id,
            "subcategory": self.subcategory.id,
            "amount": "999.00",
            "comment": self.transaction.comment,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

        self.transaction.refresh_from_db()
        self.assertEqual(self.transaction.amount, Decimal("999.00"))


    def test_transaction_delete_view_post(self):
        """Проверяем удаление транзакции"""
        url = reverse("transaction_delete", kwargs={"pk": self.transaction.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Transaction.objects.filter(pk=self.transaction.pk).exists())


    def test_categories_list(self):
        """Проверяем получение категорий по типу транзакции"""
        url = reverse("categories_list")
        response = self.client.get(url, {"transaction_type_id": self.type_expense.id})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Продукты", response.json()[0]["name"])


    def test_directory_main_view(self):
        """Проверяем доступность главной страницы справочника"""
        response = self.client.get(reverse("directory"))
        self.assertEqual(response.status_code, 200)


    def test_status_create_view(self):
        """Проверяем создание статуса в справочнике"""
        response = self.client.post(reverse("status_create"), data={"name": "Отменено"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(name="Отменено").exists())


    def test_category_delete_protect(self):
        """Проверяем, что PROTECT работает и связанную категорию нельзя удалить"""
        url = reverse("category_delete", kwargs={"pk": self.category.pk})
        response = self.client.post(url)
        self.assertIn(response.status_code, [200, 302])
        self.assertTrue(Category.objects.filter(pk=self.category.pk).exists())


class TransactionFormTests(TestCase):
    def setUp(self):
        self.status = Status.objects.create(name="Оплачено")
        self.type_expense = TransactionType.objects.create(name="Расход")
        self.type_income = TransactionType.objects.create(name="Доход")
        self.category = Category.objects.create(
            name="Продукты", transaction_type=self.type_expense
        )
        self.subcategory = SubCategory.objects.create(
            name="Хлеб", category=self.category
        )

        self.valid_data = {
            "date": "2026-06-29",
            "status": self.status.id,
            "transaction_type": self.type_expense.id,
            "category": self.category.id,
            "subcategory": self.subcategory.id,
            "amount": "150.00",
            "comment": "Тест",
        }


    def test_valid_form(self):
        """Форма валидна при корректных данных"""
        form = TransactionForm(data=self.valid_data)
        self.assertTrue(form.is_valid(), form.errors)


    def test_empty_date_defaults_to_today(self):
        """Пустая дата подставляет сегодняшнюю"""
        data = {**self.valid_data, "date": ""}
        form = TransactionForm(data=data)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["date"], date.today())


    def test_date_out_of_range(self):
        """Дата вне диапазона 2020–2050 не проходит валидацию"""
        data = {**self.valid_data, "date": "2019-12-31"}
        form = TransactionForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("date", form.errors)

        data = {**self.valid_data, "date": "2060-01-01"}
        form = TransactionForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("date", form.errors)


    def test_invalid_amount(self):
        """Нечисловая сумма не проходит валидацию"""
        data = {**self.valid_data, "amount": "abc"}
        form = TransactionForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("amount", form.errors)


    def test_amount_is_decimal(self):
        """Сумма приводится к Decimal"""
        form = TransactionForm(data=self.valid_data)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["amount"], Decimal("150.00"))


    def test_category_wrong_type(self):
        """Категория от другого типа транзакции вызывает ошибку"""
        data = {**self.valid_data, "transaction_type": self.type_income.id}
        form = TransactionForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors)


    def test_subcategory_wrong_category(self):
        """Подкатегория от другой категории вызывает ошибку"""
        other_category = Category.objects.create(
            name="Транспорт", transaction_type=self.type_expense
        )
        data = {**self.valid_data, "category": other_category.id}
        form = TransactionForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors)
