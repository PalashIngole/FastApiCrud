from fastapi import FastAPI,Depends,Path
from sqlalchemy.orm import Session
import models as models
from database import engine,get_db
from schemas import  Products

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.get("/home")
def home():
    return "Here we go in home baby"

@app.post("/product")
def create_product(product: Products,db: Session = Depends((get_db))):
    new_product = models.Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@app.get("/product")
def get_products(db: Session =Depends((get_db))):
    all_products = db.query(models.Product).all()
    return all_products

@app.get("/product/{id}")
def get_product_by_id(id: int = Path(description="product_id"), db: Session =Depends(get_db)):
    return db.query(models.Product).get(id)

@app.put("/product/{id}")
def update_product(id: int,product: Products,db: Session =Depends((get_db))):
     product_update = db.query(models.Product).get(id)
     if product_update:
         product_update.title = product.title
         product_update.description = product.description
         product_update.at_sale = product.at_sale
         product_update.inventory = product.inventory

         db.commit()
         db.close()
         return db.query(models.Product).get(id)
     else:
         return {"error": "don't exist"}


@app.delete("/product/{id}")
def update_product(id: int,db: Session =Depends((get_db))):
     product_update = db.query(models.Product).get(id)
     if product_update:
         db.delete(product_update)
         db.commit()
         db.close()
         return {"data":"product deleted"}
     else:
         return {"error": "don't exist"}










