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

## 🔥 Custom Methods in Serializers

You can add custom methods to serializers to handle specific logic. For example:

### Adding a Custom Field with Logic

```python
class VicharSerializer(serializers.ModelSerializer):
    collaborators = serializers.SerializerMethodField()

    class Meta:
        model = Vichar
        fields = ['id', 'title', 'body', 'collaborators']

    def get_collaborators(self, obj):
        collaborators = Collaborator.objects.filter(vichar=obj)
        return CollaboratorSerializer(collaborators, many=True).data
```

Usage:

By default, the `collaborators` field will be included in the serialized output. You can customize the logic in the `get_collaborators` method to return specific data.

```python
vichar = Vichar.objects.get(id=1)
serializer = VicharSerializer(vichar)
print(serializer.data)
# Output: {'id': 1, 'title': 'My Vichar', 'body': 'This is a vichar.', 'collaborators': [...]}
```

### Custom Create and Update Methods

You can override the `create` and `update` methods to customize how objects are saved:

```python
class VicharSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vichar
        fields = ['id', 'title', 'body']

    def create(self, validated_data):
        user = self.context['request'].user
        return Vichar.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        instance.updated_at = timezone.now()
        return super().update(instance, validated_data)
```

## ✨ Customizations in Serializers

Adding Validation Logic:

Custom validation can be added using the `validate_<field>` method:

```python
class VicharSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vichar
        fields = ['id', 'title', 'body']

    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters long.")
        return value
```

Using `validate` for Object-Level Validation:

You can also validate the entire object using the `validate` method:

```python
class VicharSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vichar
        fields = ['id', 'title', 'body']

    def validate(self, data):
        if data['title'] == data['body']:
            raise serializers.ValidationError("Title and body cannot be the same.")
        return data
```

## 🔒 Handling Permissions  in Serializers

You can add permission checks directly in the serializer:

```python
class VicharSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vichar
        fields = ['id', 'title', 'body']

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if instance.user != user:
            raise serializers.ValidationError("You do not have permission to edit this Vichar.")
        return super().update(instance, validated_data)
```

## 🎯 Conclusion

Serialization is a crucial part of building APIs in Django Rest Framework. By using `ModelSerializer`, custom validations, and hyperlinked relationships, you can efficiently handle data transformation and validation. 🚀
