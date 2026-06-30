from django.contrib import messages
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .crud import ref_create, ref_delete, ref_edit
from .forms import (
    StatusForm,
    CategoryForm,
    SubCategoryForm,
    TransactionForm,
    TransactionTypeForm,
    FilterForm,
)
from .models import (
    Status,
    Category,
    SubCategory,
    Transaction,
    TransactionType,
)


def transaction_list(request):
    transactions = Transaction.objects.select_related(
        "status", "transaction_type", "category", "subcategory"
    )
    filter_form = FilterForm(request.GET or None)

    if filter_form.is_valid():
        data = filter_form.cleaned_data
        if data["date_from"]:
            transactions = transactions.filter(date__gte=data["date_from"])
        if data["date_to"]:
            transactions = transactions.filter(date__lte=data["date_to"])
        if data["status"]:
            transactions = transactions.filter(status=data["status"])
        if data["transaction_type"]:
            transactions = transactions.filter(
                transaction_type=data["transaction_type"]
            )
        if data["category"]:
            transactions = transactions.filter(category=data["category"])
        if data["subcategory"]:
            transactions = transactions.filter(subcategory=data["subcategory"])

    total_in = (
        transactions.filter(transaction_type__name="Пополнение").aggregate(
            total=Sum("amount")
        )["total"]
        or 0
    )

    total_out = (
        transactions.filter(transaction_type__name="Списание").aggregate(
            total=Sum("amount")
        )["total"]
        or 0
    )

    return render(
        request,
        "dds/transaction_list.html",
        {
            "transactions": transactions,
            "filter_form": filter_form,
            "total_in": total_in,
            "total_out": total_out,
            "balance": total_in - total_out,
        },
    )


def transaction_create(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Запись успешно создана.")
            return redirect("transaction_list")
    else:
        form = TransactionForm()
    return render(
        request,
        "dds/transaction_form.html",
        {"form": form, "title": "Новая запись ДДС"},
    )


def transaction_edit(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == "POST":
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, "Запись обновлена.")
            return redirect("transaction_list")
    else:
        form = TransactionForm(instance=transaction)
    return render(
        request,
        "dds/transaction_form.html",
        {"form": form, "title": "Редактировать запись"},
    )


def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == "POST":
        transaction.delete()
        messages.success(request, "Запись удалена.")
        return redirect("transaction_list")
    return render(
        request, "dds/transaction_confirm_delete.html", {"object": transaction}
    )


def categories_list(request):
    type_id = request.GET.get("type_id")
    sub_id = request.GET.get("subcategory_id")

    qs = Category.objects.all()

    if type_id:
        qs = qs.filter(transaction_type_id=type_id)

    if sub_id:
        qs = qs.filter(subcategories__id=sub_id)

    qs = qs.distinct().order_by("id")

    return JsonResponse(
        [
            {
                "id": c.id,
                "name": c.name,
                "label": str(c),
            }
            for c in qs
        ],
        safe=False,
        json_dumps_params={"ensure_ascii": False},
    )


def subcategories_list(request):
    cat_id = request.GET.get("category_id")
    type_id = request.GET.get("type_id")

    qs = SubCategory.objects.all()

    if cat_id:
        qs = qs.filter(category_id=cat_id)

    if type_id:
        qs = qs.filter(category__transaction_type_id=type_id)

    qs = qs.distinct().order_by("id")

    return JsonResponse(
        [
            {
                "id": c.id,
                "name": c.name,
                "label": str(c),
            }
            for c in qs
        ],
        safe=False,
        json_dumps_params={"ensure_ascii": False},
    )


def directory(request):
    return render(
        request,
        "dds/directory.html",
        {
            "statuses": Status.objects.all(),
            "types": TransactionType.objects.all(),
            "categories": Category.objects.select_related("transaction_type"),
            "subcategories": SubCategory.objects.select_related(
                "category__transaction_type"
            ),
        },
    )


def status_create(request):
    return ref_create(
        request,
        StatusForm,
        "directory",
        "Добавить статус",
    )


def status_edit(request, pk):
    return ref_edit(
        request,
        get_object_or_404(Status, pk=pk),
        StatusForm,
        "directory",
        "Редактировать статус",
    )


def status_delete(request, pk):
    return ref_delete(
        request,
        get_object_or_404(Status, pk=pk),
        "directory",
    )


def type_create(request):
    return ref_create(
        request,
        TransactionTypeForm,
        "directory",
        "Добавить тип",
    )


def type_edit(request, pk):
    return ref_edit(
        request,
        get_object_or_404(TransactionType, pk=pk),
        TransactionTypeForm,
        "directory",
        "Редактировать тип",
    )


def type_delete(request, pk):
    return ref_delete(
        request,
        get_object_or_404(TransactionType, pk=pk),
        "directory",
    )


def category_create(request):
    return ref_create(
        request,
        CategoryForm,
        "directory",
        "Добавить категорию",
    )


def category_edit(request, pk):
    return ref_edit(
        request,
        get_object_or_404(Category, pk=pk),
        CategoryForm,
        "directory",
        "Редактировать категорию",
    )


def category_delete(request, pk):
    return ref_delete(
        request,
        get_object_or_404(Category, pk=pk),
        "directory",
    )


def subcategory_create(request):
    return ref_create(
        request,
        SubCategoryForm,
        "directory",
        "Добавить подкатегорию",
    )


def subcategory_edit(request, pk):
    return ref_edit(
        request,
        get_object_or_404(SubCategory, pk=pk),
        SubCategoryForm,
        "directory",
        "Редактировать подкатегорию",
    )


def subcategory_delete(request, pk):
    return ref_delete(
        request,
        get_object_or_404(SubCategory, pk=pk),
        "directory",
    )
