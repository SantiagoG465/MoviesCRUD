# MoviesCRUD API 🎬

API REST desarrollada con **FastAPI** y **Pydantic** para la gestión de géneros, películas y usuarios con almacenamiento en archivos CSV.

---

## 1. Modelos de Datos (`models.py`)

1. **`Genre`**: `id`, `name`
2. **`Movie`**: `id`, `title`, `director`, `year`, `watched`, `genre_id`
3. **`User`**: `id`, `name`, `email`, `is_active`

---

## 2. Reglas de Negocio y Eliminación con Histórico

- **Integridad de Géneros en Películas**: No se permite crear o actualizar una película con un `genre_id` que no exista en `genres.csv`.
- **Protección al Eliminar Géneros**: No se permite eliminar un género (`DELETE /genres/{id}`) si existen películas asociadas a ese género.
- **Unicidad**: No se permiten géneros con el mismo nombre ni usuarios con el mismo correo electrónico (`email`).
- **Eliminación Lógica / Histórico (`User`)**: Al eliminar un usuario (`DELETE /users/{id}`), no se borra físicamente del archivo sino que su estado cambia a `is_active = False`. Se pueden consultar usuarios activos (`GET /users/active`), inactivos (`GET /users/inactive`) o el histórico completo (`GET /users`).

---

## 3. Mapa de Endpoints

| Recurso | Método HTTP | Ruta (Endpoint) | Parámetros / Body | Descripción | Códigos de Respuesta |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Root** | `GET` | `/` | Ninguno | Mensaje de bienvenida de la API | `200 OK` |
| **Genre** | `POST` | `/genres` | Body: `GenreBase` (`name`) | Crear un nuevo género | `200 OK`, `400 Bad Request` |
| **Genre** | `GET` | `/genres` | Ninguno | Listar todos los géneros | `200 OK` |
| **Genre** | `GET` | `/genres/{id}` | Path: `id` (int) | Obtener un género por su ID | `200 OK`, `404 Not Found` |
| **Genre** | `PATCH` | `/genres/{id}` | Path: `id`, Body: `GenreUpdate` | Actualizar datos de un género | `200 OK`, `400 Bad Request`, `404 Not Found` |
| **Genre** | `DELETE` | `/genres/{id}` | Path: `id` (int) | Eliminar género (valida que no tenga películas asociadas) | `200 OK`, `400 Bad Request`, `404 Not Found` |
| **Movie** | `POST` | `/movies` | Body: `MovieBase` | Crear una película (valida que `genre_id` exista) | `200 OK`, `400 Bad Request` |
| **Movie** | `GET` | `/movies` | Ninguno | Listar todas las películas | `200 OK` |
| **Movie** | `GET` | `/movies/filter` | Query: `genre_id` (int) | **Filtrar** listado de películas por género | `200 OK`, `404 Not Found` |
| **Movie** | `GET` | `/movies/{id}` | Path: `id` (int) | Obtener una película por su ID | `200 OK`, `404 Not Found` |
| **Movie** | `PATCH` | `/movies/{id}` | Path: `id`, Body: `MovieUpdate` | Actualizar datos de una película | `200 OK`, `400 Bad Request`, `404 Not Found` |
| **Movie** | `DELETE` | `/movies/{id}` | Path: `id` (int) | Eliminar una película por su ID | `200 OK`, `404 Not Found` |
| **User** | `POST` | `/users` | Body: `UserBase` | Crear un nuevo usuario | `200 OK`, `400 Bad Request` |
| **User** | `GET` | `/users` | Ninguno | Listar todos los usuarios (histórico completo) | `200 OK` |
| **User** | `GET` | `/users/active` | Ninguno | Listar únicamente los usuarios **activos** (`is_active=True`) | `200 OK` |
| **User** | `GET` | `/users/inactive` | Ninguno | Listar únicamente los usuarios **inactivos** (`is_active=False`) | `200 OK` |
| **User** | `GET` | `/users/search` | Query: `email` (str) | **Buscar** un usuario por un atributo diferente al ID (`email`) | `200 OK`, `404 Not Found` |
| **User** | `GET` | `/users/{id}` | Path: `id` (int) | Obtener un usuario por su ID | `200 OK`, `404 Not Found` |
| **User** | `PATCH` | `/users/{id}` | Path: `id`, Body: `UserUpdate` | Actualizar datos de un usuario | `200 OK`, `400 Bad Request`, `404 Not Found` |
| **User** | `DELETE` | `/users/{id}` | Path: `id` (int) | Desactivar un usuario (`is_active=False`, conserva histórico) | `200 OK`, `404 Not Found` |
