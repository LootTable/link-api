from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
from contextlib import asynccontextmanager
# runs create_database() automatically when the server starts up
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_database()
    yield
app = FastAPI(lifespan=lifespan)
# full link model including click count — used internally
class Link(BaseModel):
    title: str
    url: str
    icon: str
    main_link: str
    click_count: int = 0
# what the user actually sends in — no click count since that starts at 0
class LinkData(BaseModel):
    title: str
    url: str
    icon: str
    main_link: str



# returns all links from the database as a list of dicts
@app.get("/links")
def get_links():
    links = []
    with sqlite3.connect("links.db") as conn:
        conn.row_factory = sqlite3.Row #lets us access columns by name instead of index
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM  links")
        results = cursor.fetchall() 
        for row in results:
            links.append(dict(row))
        return {"links": links}

# adds a new link to the database
@app.post("/links")
def post_links(link: LinkData):
    with sqlite3.connect("links.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO links (title, url, icon, main_link, click_count) VALUES (?, ?, ?, ?, 0)"
            ,(link.title, link.url,link.icon, link.main_link)
                    )
        conn.commit()
        return{"message": "Action successful"}

# deletes a link by id, returns an error if it doesn't exist
@app.delete("/links/{id}")
def delete_links(id: int):
    with sqlite3.connect("links.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM links WHERE id = ?",(id,))
        if cursor.rowcount == 0:
            return {"message": "Not found"}        
        else:
            conn.commit()
        return {"message": f"{id} has been deleted successfully"}

# updates an existing link's info by id
@app.put("/links/{id}")
def update_links(id: int, link: LinkData):
    with sqlite3.connect("links.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """UPDATE links 
            SET title = ?,
            url = ?,
            icon = ?,
            main_link = ?
            WHERE id = ?
            """,
            (link.title, link.url,link.icon, link.main_link, id)
        )
        if cursor.rowcount == 0:
            return {"message": "Nothing found"}
        else:
            conn.commit()
        return {"message": f"{link.url} has been updated"}

# increments the click count by 1 every time this endpoint is hit
@app.get("/links/{id}/click")
def clicker_counter(id: int):
    with sqlite3.connect("links.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
        UPDATE links
        set click_count = click_count + 1
        WHERE id = ?
            """
        , (id,)
        )
        if cursor.rowcount == 0:
            return {"message": "None Found"}
        else:
            conn.commit()
        return {"message": "1 click added"}

# returns total link count and total clicks across all links
@app.get("/stats")
def get_stats():
    with sqlite3.connect("links.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT COUNT(*),
            SUM(click_count) FROM links
            """)
        results = cursor.fetchone()
        return {
            "total_links": results[0],
            "total_clicks": results[1]
        }    




# creates the links table if it doesn't already exist
def create_database():
    with sqlite3.connect("links.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS links(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    url TEXT,
                    icon TEXT,
                    main_link TEXT,
                    click_count INTEGER 
                    )""")
        conn.commit()

  
@app.get("/")
def read_root():
    return {"message": "Database is ready"}
