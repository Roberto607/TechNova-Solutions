# 🛒 TechNova - E-commerce Django

## 📋 **Proyecto Django Limpio** (Solo código)

### ✅ **Incluye:**
- Estructura Django corregida (proyecto + apps)
- Templates HTML completos
- Archivos estáticos (CSS, JS, imágenes)
- Models, Views, URLs configurados
- Sistema de usuarios personalizado
- Catálogo de productos
- Carrito de compras
- Sistema de pedidos

---

## 🚀 **Instalación Rápida**

### 1️⃣ **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

### 2️⃣ **Ejecutar migraciones:**
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3️⃣ **Crear superusuario:**
```bash
python manage.py createsuperuser
```

### 4️⃣ **Ejecutar servidor:**
```bash
python manage.py runserver
```

---

## 🌐 **Acceder:**
- **Sitio web:** http://127.0.0.1:8000
- **Admin:** http://127.0.0.1:8000/admin

---

## 📁 **Estructura:**
```
technova_django_solo/
├── manage.py
├── requirements.txt
├── technova_project/ ← configuración Django
├── core/ ← funcionalidad común
├── users/ ← usuarios y autenticación  
├── products/ ← catálogo de productos
├── orders/ ← carrito y pedidos
├── templates/ ← plantillas HTML
└── static/ ← CSS, JS, imágenes
```

---

## ⚙️ **Configuración:**
- **Base de datos:** SQLite (por defecto)
- **Usuario personalizado:** `users.User`
- **Configuración:** `technova_project/settings.py`

**¡Listo para usar!** 🎉