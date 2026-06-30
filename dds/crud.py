from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import redirect, render


def ref_create(request, FormClass, redirect_name, title):
    form = FormClass(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Запись добавлена.")
        return redirect(redirect_name)
    return render(request, "dds/ref_form.html", {"form": form, "title": title})


def ref_edit(request, instance, FormClass, redirect_name, title):
    form = FormClass(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        messages.success(request, "Запись обновлена.")
        return redirect(redirect_name)
    return render(request, "dds/ref_form.html", {"form": form, "title": title})


def ref_delete(request, instance, redirect_name):
    if request.method == "POST":
        try:
            instance.delete()
            messages.success(request, "Запись удалена.")
        except ProtectedError:
            messages.error(request, "Нельзя удалить: есть связанные записи.")
        return redirect(redirect_name)
    return render(request, "dds/ref_confirm_delete.html", {"object": instance})
