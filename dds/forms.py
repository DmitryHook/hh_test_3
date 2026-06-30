from decimal import Decimal, InvalidOperation

from django import forms
from django.core.exceptions import ValidationError
from django.utils.timezone import localdate

from .models import Category, Status, SubCategory, Transaction, TransactionType


class TransactionForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(
            format="%Y-%m-%d", attrs={"type": "date", "class": "form-control", "min": "2020-01-01", "max": "2050-12-31"}
        ),
        label="Дата",
        required=False,
    )

    class Meta:
        model = Transaction
        fields = [
            "date",
            "status",
            "transaction_type",
            "category",
            "subcategory",
            "amount",
            "comment",
        ]
        widgets = {
            "status": forms.Select(attrs={"class": "form-select"}),
            "transaction_type": forms.Select(
                attrs={"class": "form-select", "id": "id_transaction_type"}
            ),
            "category": forms.Select(
                attrs={"class": "form-select", "id": "id_category"}
            ),
            "subcategory": forms.Select(
                attrs={"class": "form-select", "id": "id_subcategory"}
            ),
            "amount": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "inputmode": "decimal",
                    "autocomplete": "off",
                }
            ),
            "comment": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
        labels = {
            "status": "Статус",
            "transaction_type": "Тип",
            "category": "Категория",
            "subcategory": "Подкатегория",
            "amount": "Сумма (руб.)",
            "comment": "Комментарий",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["status"].empty_label = "Выберите статус"
        self.fields["transaction_type"].empty_label = "Выберите тип"
        self.fields["category"].empty_label = "Выберите категорию"
        self.fields["subcategory"].empty_label = "Выберите подкатегорию"

    def clean_date(self):
        date = self.cleaned_data.get("date")

        if not date:
            return localdate()

        if not 2020 <= date.year <= 2050:
            raise ValidationError("Должна быть между 2020 и 2050 годом")

        return date

    def clean_amount(self):
        value = self.cleaned_data["amount"]

        try:
            value = Decimal(value)
        except (InvalidOperation, AttributeError):
            raise ValidationError("Только числовые значения")

        return value


    def clean(self):
        cleaned_data = super().clean()
        transaction_type = cleaned_data.get("transaction_type")
        category = cleaned_data.get("category")
        subcategory = cleaned_data.get("subcategory")

        if transaction_type and category:
            if category.transaction_type != transaction_type:
                raise ValidationError(
                    f"Категория «{category.name}» не относится к типу «{transaction_type}»."
                )

        if category and subcategory:
            if subcategory.category != category:
                raise ValidationError(
                    f"Подкатегория «{subcategory.name}» не относится к категории «{category.name}»."
                )

        return cleaned_data


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ["name"]
        widgets = {"name": forms.TextInput(attrs={"class": "form-control"})}
        labels = {"name": "Название"}


class TransactionTypeForm(forms.ModelForm):
    class Meta:
        model = TransactionType
        fields = ["name"]
        widgets = {"name": forms.TextInput(attrs={"class": "form-control"})}
        labels = {"name": "Название"}


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "transaction_type"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "transaction_type": forms.Select(attrs={"class": "form-select"}),
        }
        labels = {"name": "Название", "transaction_type": "Тип операции"}


class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ["name", "category"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
        }
        labels = {"name": "Название", "category": "Категория"}


class FilterForm(forms.Form):
    date_from = forms.DateField(
        required=False,
        label="Дата с",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control", "min": "2020-01-01", "max": "2050-12-31"}),
    )
    date_to = forms.DateField(
        required=False,
        label="Дата по",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control", "min": "2020-01-01", "max": "2050-12-31"}),
    )
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        required=False,
        label="Статус",
        empty_label="Все статусы",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    transaction_type = forms.ModelChoiceField(
        queryset=TransactionType.objects.all(),
        required=False,
        label="Тип",
        empty_label="Все типы",
        widget=forms.Select(attrs={"class": "form-select", "id": "filter_type"}),
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label="Категория",
        empty_label="Все категории",
        widget=forms.Select(attrs={"class": "form-select", "id": "filter_category"}),
    )
    subcategory = forms.ModelChoiceField(
        queryset=SubCategory.objects.all(),
        required=False,
        label="Подкатегория",
        empty_label="Все подкатегории",
        widget=forms.Select(attrs={"class": "form-select", "id": "filter_subcategory"}),
    )
