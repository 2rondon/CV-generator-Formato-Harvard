import sqlite3 # <-- AGREGADO: Evita el error al capturar IntegrityError
import bcrypt
from database.connection import get_connection

class AuthController:
    
    @staticmethod
    def register_user(username, password, email=""): 
        # Reordenado y puesto 'email' como opcional con ="" 
        # para que coincida perfectamente con los datos que envía tu formulario
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Encriptación de contraseña segura
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Si no se pasó email, usamos un string vacío o un patrón básico
        if not email:
            email = f"{username}@local.com"

        try:
            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                (username, email, hashed)
            )
            user_id = cursor.lastrowid
            
            # Inicializar perfil vacío vinculado al usuario recién creado
            cursor.execute("INSERT INTO profile (user_id) VALUES (?)", (user_id,))
            conn.commit()
            return True, "Registro exitoso"
            
        except sqlite3.IntegrityError:
            return False, "El usuario o email ya existe"
            
        finally:
            conn.close()

    @staticmethod
    def login_user(username, password):
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, password FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        conn.close()
        
        if row and bcrypt.checkpw(password.encode('utf-8'), row[1].encode('utf-8')):
            return True, row[0] # Retorna el ID del usuario para mantener la sesión activa
            
        return False, "Credenciales incorrectas"