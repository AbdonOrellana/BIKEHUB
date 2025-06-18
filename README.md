# 🚴 BikeHub - Sistema de Gestión de Bicicletas

Sistema web completo para la gestión de ventas, arriendos y reparaciones de bicicletas desarrollado en Django.

## 🚀 Características

- **Gestión de Clientes**: Registro, login
- **Catálogo de Bicicletas**: Búsqueda y visualización de productos
- **Carrito de Compras**: Sistema completo de carrito y checkout
- **Sistema de Pagos**: Integración con Stripe (configurado y listo para usar)
- **Arriendos**: Gestión de arriendos de bicicletas
- **Reparaciones**: Solicitud y seguimiento de reparaciones
- **Panel de Administración**: Gestión completa del sistema
- **Gestión de Técnicos/Vendedores**: Panel específico para personal

## 📋 Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git

## 🛠️ Instalación

### 1. Clonar el repositorio
```bash
git clone <URL_DEL_REPOSITORIO>
cd bikehub
```

### 2. Crear entorno virtual
```bash
python -m venv env
```

### 3. Activar el entorno virtual

**Windows:**
```bash
env\Scripts\activate
```

**macOS/Linux:**
```bash
source env/bin/activate
```

### 4. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 5. Ejecutar migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Crear superusuario (Recomendado)
```bash
python manage.py createsuperuser
```

### 7. Ejecutar el servidor
```bash
python manage.py runserver
```

## 🌐 Acceso al Sistema

- **URL Principal**: http://127.0.0.1:8000/home
- **Admin Django**: http://127.0.0.1:8000/admin/

## 👤 Credenciales por Defecto

### Administrador
- **Email**: admin@gmail.com
- **Contraseña**: admin1234

## 📱 Uso del Sistema

### Para Clientes:
1. Registrarse en la página principal
2. Verificar email (llegará a su correo)
3. Iniciar sesión
4. Navegar por el catálogo de bicicletas
5. Agregar productos al carrito
6. Realizar checkout y pago
7. Solicitar arriendos o reparaciones

### Para Administradores:
1. Acceder con credenciales de admin
2. Gestionar usuarios, productos y órdenes
3. Ver reportes de ganancias
4. Registrar técnicos y vendedores

### Para Técnicos/Vendedores:
1. Acceder al panel específico
2. Gestionar inventario de bicicletas
3. Registrar ventas
4. Gestionar solicitudes de reparación

## 💳 Sistema de Pagos

El proyecto incluye **Stripe configurado y listo para usar** con claves de prueba:
- ✅ Pagos con tarjeta de crédito/débito (NRO tarjeta pruebas: 4242 4242 4242 4242, demás datos pueden ser cualquier numero (CSV, fecha expiración) código postal solo 5 números.)
- ✅ Webhooks configurados
- ✅ Manejo de errores de pago
- ✅ Confirmación de transacciones

**Nota**: Las claves de Stripe están configuradas para modo de prueba. Para producción, deberás reemplazarlas con tus propias claves.


### Error de pagos:
- Verificar que las claves de Stripe estén correctas
- Revisar la configuración de webhooks en Stripe
- Verificar logs del servidor para errores específicos

## 📄 Licencia

Este proyecto es de uso educativo y comercial.

## 👥 Contribución

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📞 Soporte

Para soporte técnico o preguntas, contactar al equipo de desarrollo.

---

**¡Disfruta usando BikeHub! 🚴‍♂️** 