# Django Pagination Tutorial

Pagination in Django helps manage large datasets by breaking them into smaller, manageable pages. Django provides built-in tools for pagination in both traditional views and Django REST Framework (DRF).

## 🔹 Django's Built-in Pagination

Django's `Paginator` class helps paginate querysets in a simple way.

### 1️⃣ Using Paginator in a View

#### 📝 Example: Paginating Queryset in a View

```python
from django.core.paginator import Paginator
from django.http import JsonResponse
from myapp.models import Item

def paginated_view(request):
    item_list = Item.objects.all()
    paginator = Paginator(item_list, 5)  # 5 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return JsonResponse({'items': list(page_obj.object_list.values()), 'page': page_obj.number, 'total_pages': paginator.num_pages})
```

## 🛡️ Pagination in Django REST Framework (DRF)

DRF provides built-in pagination classes that can be set globally or per view.

### 1️⃣ Setting Global Pagination in `settings.py`

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}
```

### 2️⃣ Using Different Pagination Classes

DRF provides multiple pagination styles:

- **PageNumberPagination** ➡️ Uses `page` query parameter.
- **LimitOffsetPagination** ➡️ Uses `limit` and `offset` parameters.
- **CursorPagination** ➡️ Uses opaque cursor-based pagination for efficient querying.

#### 📝 Example: Applying Pagination to a View

DRF automatically applies pagination when `pagination_class` is set in a view, so manual pagination logic is not needed:

```python
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from myapp.models import Item
from myapp.serializers import ItemSerializer

class PaginatedViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    pagination_class = PageNumberPagination  # DRF handles pagination automatically
```

### 3️⃣ Custom Pagination Classes

You can create custom pagination classes by extending DRF's base classes. For example, you can customize the `PageNumberPagination` class to change the default page size or add additional metadata to the response.

```python
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })
```

Example usage in a view:

```python
from rest_framework.viewsets import ModelViewSet
from myapp.models import Item
from myapp.serializers import ItemSerializer
from myapp.pagination import CustomPageNumberPagination

class CustomPaginatedViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    pagination_class = CustomPageNumberPagination  # Use custom pagination class
```

## Usage of Pagination Classes

- **PageNumberPagination**: Simple and easy to use, suitable for small datasets.
- **LimitOffsetPagination**: More flexible, allows clients to specify the number of items to skip and limit.
- **CursorPagination**: Best for large datasets, provides better performance and consistency.
- **Custom Pagination**: You can create custom pagination classes by extending DRF's base classes.

## 📌 Best Practices for Pagination

- ✅ **Choose the appropriate pagination type based on data size and query performance**
- ✅ **Set global pagination settings for consistency**
- ✅ **Ensure API consumers understand pagination response structure**
- ✅ **Use CursorPagination for large datasets to improve performance**

---

📖 This tutorial covers Django pagination, including built-in pagination, DRF pagination methods, and best practices. Implementing pagination ensures better user experience and performance in handling large datasets. 🚀

[🔙 Back to Main Docs](./README.md)
