# 🔄 Serialization in Django Rest Framework (DRF) 📜

## 🤔 What is Serialization?

Serialization is the process of converting complex data types (such as Django models) into JSON or other content types that can be easily shared over the web. DRF provides powerful serializers to transform and validate data efficiently. ✅

For more details, refer to the official [DRF Serialization documentation](https://www.django-rest-framework.org/api-guide/serializers/).

## 📂 Example: `vichar/serializers.py`

Here’s an example of how you can use serializers in a Django project: **[`vichar/serializers.py`](../vichar/serializers.py)**

## 🔑 Key Features of DRF Serialization

- 📦 **Model Serialization**: Automatically converts Django model instances into JSON.
- 🛡 **Validation**: Ensures incoming data meets the required format.
- 🔄 **Custom Serialization**: Allows modifying how data is represented.
- 🔗 **Hyperlinked Relationships**: Connects related models efficiently.

## 🚀 Creating a Serializer

DRF provides the `serializers` module to define serializers. There are two main types:

### 1️⃣ Basic Serializer

A simple serializer without a model:

```python
from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField(max_length=255)
    email = serializers.EmailField()
```

### 2️⃣ ModelSerializer (Recommended for Models)

`ModelSerializer` automates serialization for Django models:

```python
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
```

## 🛠 Using a Serializer

Serializing an object:

```python
user = User.objects.get(id=1)
serializer = UserSerializer(user)
print(serializer.data)  # Output: {'id': 1, 'username': 'john', 'email': 'john@example.com'}
```

Deserializing data:

```python
data = {'id': 1, 'username': 'john', 'email': 'john@example.com'}
serializer = UserSerializer(data=data)
if serializer.is_valid():
    user = serializer.save()
```

## 🔥 Validations in Serializers

Custom validation using the `validate_<field>` method:

```python
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
    
    def validate_username(self, value):
        if 'admin' in value.lower():
            raise serializers.ValidationError("Username cannot contain 'admin'")
        return value
```

## 🔗 HyperlinkedModelSerializer

Hyperlinked serializers use URLs instead of primary keys:

```python
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email']
```

## 🎯 Conclusion

Serialization is a crucial part of building APIs in Django Rest Framework. By using `ModelSerializer`, custom validations, and hyperlinked relationships, you can efficiently handle data transformation and validation. 🚀