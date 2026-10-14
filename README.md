# API de Doctores y Pacientes (FastAPI)

API REST en Python para registrar doctores, autenticarlos con JWT y gestionar pacientes. Al crear un paciente se puede asignar automáticamente al doctor con menos pacientes a cargo.

## Funcionalidades

- Registro de doctores con contraseña cifrada (bcrypt vía Passlib).
- Login con `cedula` y contraseña; devuelve un token JWT (HS256) que expira en 60 minutos.
- CRUD de doctores y pacientes.
- Asignación automática de doctor al paciente según la menor carga de pacientes.
- Creación automática de las tablas en MySQL al iniciar la aplicación.
- Documentación interactiva en `/docs` (Swagger UI).

## Tecnologías

Python 3.8+ · FastAPI · SQLAlchemy · MySQL · JWT · Passlib (bcrypt) · Uvicorn

## Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/auth/register` | Registrar un doctor |
| POST | `/auth/login` | Iniciar sesión y obtener token |
| POST | `/doctors/` | Crear doctor |
| GET | `/doctors/` | Listar doctores |
| GET | `/doctors/{id}` | Ver un doctor |
| DELETE | `/doctors/{id}` | Eliminar un doctor |
| POST | `/pacientes/` | Crear paciente |
| POST | `/pacientes/{paciente_id}/asignar` | Asignar doctor al paciente |
| PUT | `/pacientes/{id}` | Actualizar paciente |
| GET | `/pacientes/` | Listar pacientes |
| GET | `/pacientes/{id}` | Ver un paciente |
| DELETE | `/pacientes/{id}` | Eliminar un paciente |

## Estructura

```
backend/app/
├── main.py          # Aplicación FastAPI y registro de rutas
├── api/             # Rutas: auth, doctor, paciente
├── db/              # Conexión y modelos (Doctor, Paciente)
├── schemas/         # Esquemas Pydantic
└── services/        # Autenticación y asignación de doctor
```

## Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/pagarcia22/COMPANY-IN.git
cd COMPANY-IN
```

2. Crea y activa un entorno virtual:

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

3. Instala las dependencias:

```bash
pip install -r requirements.txt
```

4. Crea una base de datos en MySQL y copia `.env.example` a `.env` con tus datos:

```
MYSQL_USER=tu_usuario
MYSQL_PASSWORD=tu_contraseña
MYSQL_HOST=localhost
MYSQL_DB=nombre_de_tu_base
SECRET_KEY=una_clave_larga_y_aleatoria
```

5. Inicia el servidor desde la carpeta `backend`:

```bash
cd backend
uvicorn app.main:app --reload
```

6. Abre `http://127.0.0.1:8000/docs` para probar la API.

## Seguridad

No subas tu archivo `.env` al repositorio. Está incluido en `.gitignore`.

## Próximos pasos

- Proteger con JWT los endpoints de doctores y pacientes.
- Agregar pruebas automáticas con pytest.
- Agregar migraciones con Alembic.

## Licencia

MIT. Copyright (c) 2025 Paola Andrea Garcia Diaz.
