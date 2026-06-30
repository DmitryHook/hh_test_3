from django.urls import path

from . import views


urlpatterns = [
    path("", views.transaction_list, name="transaction_list"),

    path("create/", views.transaction_create, name="transaction_create"),
    path("<int:pk>/edit/", views.transaction_edit, name="transaction_edit"),
    path("<int:pk>/delete/", views.transaction_delete, name="transaction_delete"),

    path("api/categories/", views.categories_list, name="categories_list"),
    path("api/subcategories/", views.subcategories_list, name="subcategories_list"),

    path("directory/", views.directory, name="directory"),

    path("directory/status/create/", views.status_create, name="status_create"),
    path("directory/status/<int:pk>/edit/", views.status_edit, name="status_edit"),
    path("directory/status/<int:pk>/delete/", views.status_delete, name="status_delete"),

    path("directory/type/create/", views.type_create, name="type_create"),
    path("directory/type/<int:pk>/edit/", views.type_edit, name="type_edit"),
    path("directory/type/<int:pk>/delete/", views.type_delete, name="type_delete"),

    path("directory/category/create/", views.category_create, name="category_create"),
    path("directory/category/<int:pk>/edit/", views.category_edit, name="category_edit"),
    path("directory/category/<int:pk>/delete/", views.category_delete, name="category_delete"),

    path("directory/subcategory/create/", views.subcategory_create, name="subcategory_create"),
    path("directory/subcategory/<int:pk>/edit/", views.subcategory_edit, name="subcategory_edit"),
    path("directory/subcategory/<int:pk>/delete/", views.subcategory_delete, name="subcategory_delete"),
]
