import os
import jwt
from dotenv import load_dotenv
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from ..db.database import get_db
from ..db.models import Doctor



# Configuración de seguridad
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("Falta la variable de entorno SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Hasheo de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(contraseña: str) -> str:
    """Genera un hash de la contraseña antes de guardarla"""
    return pwd_context.hash(contraseña)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si la contraseña ingresada es correcta comparándola con la encriptada"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(doctor_id: int) -> str:
    """Genera un token JWT con el ID del doctor y una expiración."""
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(doctor_id),  # ID del médico
        "exp": expire  # Fecha de expiración
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def get_medico_actual(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Verifica el token JWT y obtiene el médico autenticado"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        doctor_id = payload.get("sub")
        exp = payload.get("exp")

        if doctor_id is None:
            raise HTTPException(status_code=401, detail="Token inválido: ID no encontrado")
        
        # para mi futura yo
        #recuerda pao que es para validar que el token no haya expirado
        if datetime.utcnow().timestamp() > exp:
            raise HTTPException(status_code=401, detail="Token expirado")

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")

    doctor = db.query(Doctor).filter(Doctor.id == int(doctor_id)).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor no encontrado")

    return doctor    

        