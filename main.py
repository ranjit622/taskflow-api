from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database import get_connection, create_tables
from auth import hash_password, verify_password, create_token, verify_token
from models import UserRegister, TaskCreate, TaskUpdate

# FastAPI app banao
app = FastAPI()

# Server start hote hi tables ban jayengi
create_tables()

# Token ka rasta batao — login se milega
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Current user nikalo token se
def get_current_user(token: str = Depends(oauth2_scheme)):
    # Token verify karo
    payload = verify_token(token)
    if payload is None:
        # Token galat hai — access band!
        raise HTTPException(status_code=401, detail="Invalid token!")
    return payload

# ─── AUTH ENDPOINTS ───────────────────────────────

# Register endpoint
@app.post("/register")
def register(user: UserRegister):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Password hash karke save karo
        hashed = hash_password(user.password)
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (user.username, hashed)
        )
        conn.commit()
        return {"message": "Register ho gaya!"}
    except:
        # Username pehle se hai toh error
        raise HTTPException(status_code=400, detail="Username pehle se hai!")
    finally:
        conn.close()

# Login endpoint
@app.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends()):
    conn = get_connection()
    cursor = conn.cursor()

    # User dhundo database mein
    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (form.username,)
    )
    user = cursor.fetchone()
    conn.close()

    # User nahi mila ya password galat
    if not user or not verify_password(form.password, user[2]):
        raise HTTPException(status_code=400, detail="Username ya password galat!")

    # Token banao aur bhejo
    token = create_token({"sub": str(user[0]), "username": user[1]})
    return {"access_token": token, "token_type": "bearer"}

# ─── TASKS ENDPOINTS ──────────────────────────────

# Saari tasks dekho — sirf apni!
@app.get("/tasks")
def get_tasks(current_user: dict = Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor()

    # Sirf is user ki tasks nikalo
    cursor.execute(
        "SELECT * FROM tasks WHERE user_id = ?",
        (current_user["sub"],)
    )
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "id": r[0],
            "title": r[1],
            "description": r[2],
            "completed": bool(r[3]),
            "user_id": r[4]
        }
        for r in rows
    ]

# Nayi task add karo
@app.post("/tasks")
def add_task(task: TaskCreate, current_user: dict = Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor()

    # Task database mein save karo
    cursor.execute(
        "INSERT INTO tasks (title, description, user_id) VALUES (?, ?, ?)",
        (task.title, task.description, current_user["sub"])
    )
    conn.commit()
    conn.close()
    return {"message": "Task add ho gayi!"}

# Task update karo
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate, current_user: dict = Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor()

    # Sirf apni task update kar sakta hai
    cursor.execute("""
        UPDATE tasks
        SET title=?, description=?, completed=?
        WHERE id=? AND user_id=?
    """, (task.title, task.description, int(task.completed), task_id, current_user["sub"]))
    conn.commit()
    conn.close()
    return {"message": "Task update ho gayi!"}

# Task delete karo
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, current_user: dict = Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor()

    # Sirf apni task delete kar sakta hai
    cursor.execute(
        "DELETE FROM tasks WHERE id=? AND user_id=?",
        (task_id, current_user["sub"])
    )
    conn.commit()
    conn.close()
    return {"message": "Task delete ho gayi!"}