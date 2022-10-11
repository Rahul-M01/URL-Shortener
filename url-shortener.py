from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session 
import models, schemas, CRUD
from database import SessionLocal, engine 
import validators
import secrets

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")

def raise_bad_request():
    raise HTTPException(status_code=400, detail="Bad Request")

def read_root():
    return "Welcome to the URL shortener API :)"

@app.post("/url", response_model=schemas.URLInfo)
def url_shortener(url: schemas.URLBase, db: Session = Depends(get_db)):
    if not validators.url(url.target_url):
        raise_bad_request(message="Your provided URL is not valid")
    db_url = CRUD.create_db_url(db=db, url=url)
    db_url.url = f"https://urlshortit.herokuapp.com/{db_url.key}"
    db_url.admin_url = db_url.secret_key
    return db_url

def raise_not_found(request):

    message = f"URL '{request.url}' doesn't exist"

    raise HTTPException(status_code=404, detail=message)

@app.get("/{url_key}")

def forward_to_target_url(
        url_key: str,
        request: Request,
        db: Session = Depends(get_db)
    ):

    db_url = (
        db.query(models.URL)
        .filter(models.URL.key == url_key, models.URL.is_active)
        .first()
    )

    if db_url := CRUD.get_db_url_by_key(db=db, url_key=url_key):
        return RedirectResponse(db_url.target_url)
    else:
        raise_not_found(request)



