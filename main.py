import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import db, create_document, get_documents
from schemas import LiveChannel, Video, Show, Genre, EventTicket, PurchaseRequest, PurchaseResponse

app = FastAPI(title="Avang Platform API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Utility: collection name from schema class
COLLECTIONS = {
    "livechannel": "livechannel",
    "video": "video",
    "show": "show",
    "genre": "genre",
    "eventticket": "eventticket",
}


@app.get("/")
def read_root():
    return {"name": "Avang API", "version": "1.0.0"}


@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": "❌ Not Set",
        "database_name": "❌ Not Set",
        "connection_status": "Not Connected",
        "collections": [],
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, "name") else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                response["collections"] = db.list_collection_names()
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:80]}"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"
    return response


# Seed sample data if collections are empty
@app.on_event("startup")
def seed_sample_data():
    if db is None:
        return
    try:
        if db[COLLECTIONS["genre"]].count_documents({}) == 0:
            db[COLLECTIONS["genre"]].insert_many([
                {"name": "Hip-Hop", "description": "Beats and bars", "cover": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4"},
                {"name": "Afrobeats", "description": "Rhythm from the motherland", "cover": "https://images.unsplash.com/photo-1511379938547-c1f69419868d"},
                {"name": "R&B", "description": "Smooth and soulful", "cover": "https://images.unsplash.com/photo-1516280440614-37939bbacd81"},
            ])
        if db[COLLECTIONS["livechannel"]].count_documents({}) == 0:
            db[COLLECTIONS["livechannel"]].insert_many([
                {
                    "name": "Avang Live",
                    "stream_url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8",
                    "thumbnail": "https://images.unsplash.com/photo-1495567720989-cebdbdd97913",
                    "description": "24/7 programming from Avang TV",
                }
            ])
        if db[COLLECTIONS["video"]].count_documents({}) == 0:
            db[COLLECTIONS["video"]].insert_many([
                {
                    "title": "Latest Music Video",
                    "artist": "Avang",
                    "thumbnail": "https://images.unsplash.com/photo-1521335629791-ce4aec67dd53",
                    "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
                    "genre": "R&B",
                }
            ])
        if db[COLLECTIONS["show"]].count_documents({}) == 0:
            db[COLLECTIONS["show"]].insert_many([
                {
                    "title": "Friday Night Live",
                    "synopsis": "Weekly live performance and interviews.",
                    "schedule": "Fridays 8pm GMT",
                    "poster": "https://images.unsplash.com/photo-1459749411175-04bf5292ceea",
                }
            ])
        if db[COLLECTIONS["eventticket"]].count_documents({}) == 0:
            db[COLLECTIONS["eventticket"]].insert_many([
                {
                    "event_id": "AVANG-001",
                    "event_name": "Avang Launch Concert",
                    "date": "2025-12-01",
                    "price_matic": 25.0,
                    "poster": "https://images.unsplash.com/photo-1518972559570-7cc1309f3229",
                    "venue": "Virtual Arena",
                }
            ])
    except Exception:
        # Silent fail to avoid startup crash in case of restricted DB perms
        pass


# Response models for listing endpoints
class ListResponse(BaseModel):
    items: list


@app.get("/api/live-channels", response_model=ListResponse)
def list_live_channels():
    docs = get_documents(COLLECTIONS["livechannel"]) if db else []
    # Convert ObjectId to str for frontend
    for d in docs:
        if "_id" in d:
            d["_id"] = str(d["_id"])
    return {"items": docs}


@app.post("/api/live-channels")
def create_live_channel(channel: LiveChannel):
    _id = create_document(COLLECTIONS["livechannel"], channel)
    return {"id": _id}


@app.get("/api/videos", response_model=ListResponse)
def list_videos():
    docs = get_documents(COLLECTIONS["video"]) if db else []
    for d in docs:
        if "_id" in d:
            d["_id"] = str(d["_id"])
    return {"items": docs}


@app.post("/api/videos")
def create_video(video: Video):
    _id = create_document(COLLECTIONS["video"], video)
    return {"id": _id}


@app.get("/api/shows", response_model=ListResponse)
def list_shows():
    docs = get_documents(COLLECTIONS["show"]) if db else []
    for d in docs:
        if "_id" in d:
            d["_id"] = str(d["_id"])
    return {"items": docs}


@app.post("/api/shows")
def create_show(show: Show):
    _id = create_document(COLLECTIONS["show"], show)
    return {"id": _id}


@app.get("/api/genres", response_model=ListResponse)
def list_genres():
    docs = get_documents(COLLECTIONS["genre"]) if db else []
    for d in docs:
        if "_id" in d:
            d["_id"] = str(d["_id"])
    return {"items": docs}


@app.post("/api/genres")
def create_genre(genre: Genre):
    _id = create_document(COLLECTIONS["genre"], genre)
    return {"id": _id}


@app.get("/api/tickets", response_model=ListResponse)
def list_tickets():
    docs = get_documents(COLLECTIONS["eventticket"]) if db else []
    for d in docs:
        if "_id" in d:
            d["_id"] = str(d["_id"])
    return {"items": docs}


@app.post("/api/tickets")
def create_ticket(ticket: EventTicket):
    _id = create_document(COLLECTIONS["eventticket"], ticket)
    return {"id": _id}


@app.post("/api/purchase", response_model=PurchaseResponse)
def purchase_ticket(req: PurchaseRequest):
    # NOTE: In a real implementation, this would create a transaction on Polygon (e.g., via a smart contract)
    # Here we return a mock response so the frontend can integrate wallet UI later.
    if not req.wallet_address.lower().startswith("0x"):
        raise HTTPException(status_code=400, detail="Invalid wallet address")
    fake_tx = "0x" + os.urandom(16).hex()
    return PurchaseResponse(status="success", tx_hash=fake_tx, network="polygon", token_symbol="AT")


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
