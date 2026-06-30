from django.db import models
from django.utils.timezone import localdate


class Status(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"
        ordering = ["name"]

    def __str__(self):
        return self.name


class TransactionType(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Тип операции"
        verbose_name_plural = "Типы операций"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    transaction_type = models.ForeignKey(
        TransactionType,
        on_delete=models.CASCADE,
        related_name="categories",
        verbose_name="Тип операции",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]
        unique_together = ["name", "transaction_type"]

    def __str__(self):
        return f"{self.name} ({self.transaction_type})"


class SubCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="subcategories",
        verbose_name="Категория",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
        ordering = ["name"]
        unique_together = ["name", "category"]

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class Transaction(models.Model):
    date = models.DateField(default=localdate, verbose_name="Дата")
    status = models.ForeignKey(
        Status, on_delete=models.PROTECT, verbose_name="Статус", null=True, blank=True
    )
    transaction_type = models.ForeignKey(
        TransactionType, on_delete=models.PROTECT, verbose_name="Тип"
    )
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, verbose_name="Категория"
    )
    subcategory = models.ForeignKey(
        SubCategory, on_delete=models.PROTECT, verbose_name="Подкатегория"
    )
    amount = models.DecimalField(
        max_digits=15, decimal_places=2, verbose_name="Сумма (руб.)"
    )
    comment = models.TextField(blank=True, default="", verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Запись ДДС"
        verbose_name_plural = "Записи ДДС"
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return f"{self.date} | {self.transaction_type} | {self.amount} руб."
