from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db, User, create_db_tables, Base, engine
from auth import get_password_hash, verify_password, create_access_token, decode_access_token
from schemas import UserCreate, Token
from ai import generate_ai_content
from schemas import GeneratePostRequest, PostCreate, Post
from database import Post as DBPost
from typing import List
from datetime import datetime

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configuración CORS más completa
origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:5000",
    "http://127.0.0.1:5000",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost",
    "http://127.0.0.1",
    "https://ai-blog1.onrender.com",
    "https://ai-blog1.netlify.app",
    "file://"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    return current_user

@app.post("/register", response_model=Token)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    new_user = User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    access_token = create_access_token(data={"sub": new_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/generate-post", response_model=Post, status_code=status.HTTP_201_CREATED)
async def generate_post(request: GeneratePostRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    try:
        generated_content = generate_ai_content(request.prompt)
        # For simplicity, let's assume the first line is the title and the rest is content
        lines = generated_content.split('\n', 1)
        title = lines[0] if lines else "Generated Post"
        content = lines[1] if len(lines) > 1 else "No content generated."

        # Usar string vacío si author_name es None o no está presente
        author_name = request.author_name if request.author_name else ""
        
        # Crear el post
        db_post = DBPost(
            title=title, 
            content=content, 
            owner_id=current_user.id,
            is_public=request.is_public,
            author_name=author_name  # Siempre string, nunca None
        )
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return db_post
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating post: {str(e)}"
        )

@app.get("/posts", response_model=List[Post])
async def get_posts(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    posts = db.query(DBPost).filter(DBPost.owner_id == current_user.id).all()
    return posts

@app.get("/posts/public", response_model=List[Post])
async def get_public_posts(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    public_posts = db.query(DBPost).filter(
        DBPost.is_public == True,
        DBPost.owner_id != current_user.id
    ).all()
    return public_posts

@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_post = db.query(DBPost).filter(DBPost.id == post_id).first()

    if db_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    if db_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this post")

    db.delete(db_post)
    db.commit()
    return
