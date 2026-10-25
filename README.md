# MoviesCRUD API 🎬

API REST desarrollada con **FastAPI** y **Pydantic** para la gestión de géneros, directores y películas con almacenamiento en archivos CSV.

---

## 1. Modelos de Datos (`models.py`)

1. **`Genre`**: `id`, `name`
2. **`Director`**: `id`, `name`, `nationality`, `is_active`
3. **`Movie`**: `id`, `title`, `director_id`, `year`, `watched`, `genre_id`

---

## 2. Reglas de Negocio y Eliminación con Histórico

- **Integridad de Géneros y Directores en Películas**: No se permite crear o actualizar una película con un `genre_id` o `director_id` que no exista, ni asignar un director inactivo (`is_active = False`).
- **Protección al Eliminar Géneros**: No se permite eliminar un género (`DELETE /genres/{id}`) si existen películas asociadas a ese género.
- **Unicidad**: No se permiten géneros ni directores con el mismo nombre.
- **Eliminación Lógica / Histórico (`Director`)**: Al eliminar un director (`DELETE /directors/{id}`), no se borra físicamente del archivo sino que su estado cambia a `is_active = False`. Se pueden consultar directores activos (`GET /directors/active`), inactivos (`GET /directors/inactive`) o el histórico completo (`GET /directors`).

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
| **Movie** | `POST` | `/movies` | Body: `MovieBase` | Crear una película (valida que `genre_id` y `director_id` existan) | `200 OK`, `400 Bad Request` |
| **Movie** | `GET` | `/movies` | Ninguno | Listar todas las películas | `200 OK` |
| **Movie** | `GET` | `/movies/filter` | Query: `genre_id` (int) | **Filtrar** listado de películas por género | `200 OK`, `404 Not Found` |
| **Movie** | `GET` | `/movies/{id}` | Path: `id` (int) | Obtener una película por su ID | `200 OK`, `404 Not Found` |
| **Movie** | `PATCH` | `/movies/{id}` | Path: `id`, Body: `MovieUpdate` | Actualizar datos de una película | `200 OK`, `400 Bad Request`, `404 Not Found` |
| **Movie** | `DELETE` | `/movies/{id}` | Path: `id` (int) | Eliminar una película por su ID | `200 OK`, `404 Not Found` |
| **Director** | `POST` | `/directors` | Body: `DirectorBase` | Crear un nuevo director | `200 OK`, `400 Bad Request` |
| **Director** | `GET` | `/directors` | Ninguno | Listar todos los directores (histórico completo) | `200 OK` |
| **Director** | `GET` | `/directors/active` | Ninguno | Listar únicamente los directores **activos** (`is_active=True`) | `200 OK` |
| **Director** | `GET` | `/directors/inactive` | Ninguno | Listar únicamente los directores **inactivos** (`is_active=False`) | `200 OK` |
| **Director** | `GET` | `/directors/search` | Query: `name` (str) | **Buscar** un director por un atributo diferente al ID (`name`) | `200 OK`, `404 Not Found` |
| **Director** | `GET` | `/directors/{id}` | Path: `id` (int) | Obtener un director por su ID | `200 OK`, `404 Not Found` |
| **Director** | `PATCH` | `/directors/{id}` | Path: `id`, Body: `DirectorUpdate` | Actualizar datos de un director | `200 OK`, `400 Bad Request`, `404 Not Found` |
| **Director** | `DELETE` | `/directors/{id}` | Path: `id` (int) | Desactivar un director (`is_active=False`, conserva histórico) | `200 OK`, `404 Not Found` |
