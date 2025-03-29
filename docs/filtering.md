# Django Filtering Tutorial

Filtering in Django REST Framework (DRF) allows users to refine API responses by applying filters, search parameters, and ordering.

For more information, refer to the official [DRF documentation](https://www.django-rest-framework.org/api-guide/filtering/).

## 🔹 Using Django Filters

Django provides the `django-filter` package to enable filtering capabilities in DRF views.

### 1️⃣ Setting Up Filtering in DRF

First, install `django-filter`:

```bash
pip install django-filter
```

Then, add it to `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    ...
    'django_filters',
]
```

Also, configure it in DRF settings:

```python
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}
```

## 2️⃣ Basic Filtering

You can filter querysets using the `filterset_fields` attribute in your view. For example:

```python
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from myapp.models import Product
from myapp.serializers import ProductSerializer
from rest_framework.permissions import IsAuthenticated

class ProductListView(generics.ListAPIView):
    """
    Product List View for listing and filtering products.
    
    The view is inherited from ListAPIView. It lists all products and supports filtering.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    # Filters
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'price': ['exact', 'gte', 'lte'],
        'category': ['exact', 'icontains'],
        'sold': ['exact'],
    }
```

Explanation of the filter fields:

- `price`: Filters products with exact price, greater than or equal to (`gte`), or less than or equal to (`lte`) the specified value.
- `category`: Filters products with exact category or case-insensitive match (`icontains`).
- `sold`: Filters products based on their sold status (true or false).

## 3️⃣ Advanced Filtering

You can create more complex filters using `FilterSet` classes. This allows you to define custom filters and their behavior.

### 🛠️ Custom Filter Class

You can create custom filters to allow more advanced filtering options. Below is an example of a `ProductFilter` class:

```python
import django_filters
from django_filters.rest_framework import FilterSet
from myapp.models import Product

class ProductFilter(FilterSet):
    """
    Filter class for Product model to filter products.

    - min_price: Filter products with price greater than or equal to the given value.
    - max_price: Filter products with price less than or equal to the given value.
    - category: Filter products with the given category with case-insensitive match.
    - sold: Filter products with the given sold value (true or false).
    """

    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    category = django_filters.CharFilter(field_name="category", lookup_expr="iexact")

    class Meta:
        model = Product
        fields = {
            "sold": ["exact"],
        }
```

## 🔍 Search and Ordering

Apart from filtering, DRF allows search and ordering using built-in filters.

- **SearchFilter** ➡️ Enables searching based on specific fields.
- **OrderingFilter** ➡️ Allows sorting the results based on given fields.

### 📝 Example: Applying Filters, Search, and Ordering

```python
from rest_framework import filters, generics
from django_filters.rest_framework import DjangoFilterBackend
from myapp.models import Product
from myapp.serializers import ProductSerializer
from myapp.filters import ProductFilter
from rest_framework.permissions import IsAuthenticated

class ProductListView(generics.ListAPIView):
    """
    Product List View for listing and filtering products.
    
    The view is inherited from ListAPIView. It lists all products and supports filtering, searching, and ordering.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    # Filters
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_class = ProductFilter

    # Search fields
    search_fields = ["title"]

    # Ordering fields
    ordering_fields = ["price", "title"]
```

## 🚀 Usage

To use filtering, searching, and ordering in API requests, you can pass query parameters in the URL.

### 🔹 Example API Endpoints

#### Filtering

```bash
GET /api/products/?min_price=100&max_price=500
```

#### Searching

```bash
GET /api/products/?search=Smartphone
```

#### Ordering

```bash
GET /api/products/?ordering=price  # Ascending order
GET /api/products/?ordering=-price  # Descending order
```

## 📌 Best Practices for Filtering

- ✅ **Use a `FilterSet` class to keep filtering logic clean**
- ✅ **Enable search and ordering for better user experience**
- ✅ **Document the available filters in API documentation**
- ✅ **Use indexing on frequently filtered fields for performance optimization**

---

📖 This tutorial covered Django filtering, search, and ordering using `django-filter` and DRF's built-in capabilities. Implementing proper filtering ensures better usability and performance. 🚀

[🔙 Back to Main Docs](./README.md)
