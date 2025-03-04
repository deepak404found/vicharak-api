# Vicharak

Vicharak is a collaborative platform that allows users to create, manage, and share thoughts or ideas (Vichars) while controlling access through a role-based permission system. It enables multiple users to collaborate on a Vichar with predefined roles and permissions.

---

## **📚 Entities**

Here’s a structured documentation for all the entities in system:

## **1️⃣ Users**

### **Description**  

Users are the primary entity in the system. They can create Vichars, manage collaborations, and perform actions based on their assigned roles.

### **Permissions**

✅ Users can **Create, Read, Update, and Delete (CRUD)** their own profile.  
✅ Users can **create Vichars**.  
✅ Users can **be added as collaborators** to a Vichar with a specific role.  

---

## **2️⃣ Roles**

### **Description**  

Roles define a set of permissions that can be assigned to users when they collaborate on a Vichar.

### **Fields**

- `name` (string) - The name of the role (e.g., Editor, Viewer).
- `permissions` (list) - A list of permissions granted to this role.

### **Example Permissions**

| Permission            | Description                              |
| --------------------- | ---------------------------------------- |
| `VIEW_VICHAR`         | Allows viewing a Vichar                  |
| `EDIT_VICHAR`         | Allows editing a Vichar                  |
| `DELETE_VICHAR`       | Allows deleting a Vichar                 |
| `ADD_COLLABORATOR`    | Allows adding collaborators              |
| `REMOVE_COLLABORATOR` | Allows removing collaborators            |
| `VIEW_COLLABORATORS`  | Allows viewing the list of collaborators |

### **Permissions for Role Management**

✅ Only **staff users** can create or manage roles.  

---

## **3️⃣ Vichars**

### **Description**  

A Vichar represents a thought or idea created by a user.

### **Fields**

- `user` (ForeignKey to User) - The creator of the Vichar.
- `title` (string) - Title of the Vichar.
- `body` (text) - The content of the Vichar.
- `created_at` (datetime) - Timestamp when the Vichar was created.
- `updated_at` (datetime) - Timestamp when the Vichar was last updated.
- `deleted_at` (datetime, nullable) - If deleted, stores the deletion timestamp.

### **Permissions**

✅ The **owner of a Vichar** can perform **CRUD operations**.  
✅ **Collaborators** can perform actions based on their assigned **role permissions**.  
❌ **Unauthorized users cannot access private Vichars**.  

---

## **4️⃣ Collaborators**

### **Description**  

Collaborators are users who are invited to work on a Vichar with a specific role.

### **Fields**

- `vichar` (ForeignKey to Vichar) - The Vichar the user is collaborating on.
- `owner` (ForeignKey to User) - The user who owns the Vichar.
- `collaborator` (ForeignKey to User) - The user being added as a collaborator.
- `role` (ForeignKey to Role) - The assigned role of the collaborator.
- `created_at` (datetime) - Timestamp when the collaborator was added.

### **Permissions**

✅ **Only the Vichar owner** can add or remove collaborators.  
✅ **Collaborators can perform actions** based on the **role assigned to them**.  

---

# **🔗 Relationships Between Entities**

- A **User** can create multiple **Vichars**.
- A **Vichar** can have multiple **Collaborators**.
- A **Collaborator** has a **Role**, which defines their permissions.
- Only **Staff Users** can **manage roles**.
