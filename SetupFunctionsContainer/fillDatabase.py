"""Seed travel.db: hotels, availabilities, and space_travel_vectors (sqlite-vec).

Run from the project root:
    python -m SetupFunctionsContainer.fillDatabase

Requires AZURE_OPENAI_API_KEY / AZURE_OPENAI_ENDPOINT / OPENAI_API_VERSION env vars.
"""
import os
import struct
import sqlite3
from pathlib import Path

import sqlite_vec
import tiktoken
from openai import AzureOpenAI

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "travel.db"
SPACE_DIR = ROOT / "Space Destinations"
EMBEDDING_DIM = 3072
EMBEDDING_MODEL = "text-embedding-3-large"

tokenizer = tiktoken.encoding_for_model("gpt-4o")
client = AzureOpenAI()

LOCATION_BY_FOLDER = {
    "Luna": "Luna",
    "Mars": "Mars",
    "MASSAGE-2(A-B)b": "Massage",
}

HOTEL_PRICE_BY_TYPE = {
    "family_hotel": 150,
    "luxury": 400,
    "hostel": 50,
}

# Hardcoded availability windows so book_hotel always has something to find.
AVAILABILITY_WINDOWS = [
    ("2027-05-01", "give_tourist_information_space_description2027-05-31"),
    ("2027-07-01", "2027-08-15"),
    ("2027-10-10", "2027-11-30"),
]


def pack_vector(values):
    return struct.pack(f"{len(values)}f", *values)


def chunker(text):
    words = text.replace("\n", " ").split()
    chunk_length = 128
    current_chunk = []
    current_chunk_length = 0
    chunks = []
    for word in words:
        word_tokens = tokenizer.encode(word + " ")
        word_length = len(word_tokens)
        if current_chunk_length + word_length > chunk_length:
            chunks.append(current_chunk)
            current_chunk = word_tokens
            current_chunk_length = word_length
        else:
            current_chunk.extend(word_tokens)
            current_chunk_length += word_length
    if current_chunk:
        chunks.append(current_chunk)
    return [tokenizer.decode(chunk) for chunk in chunks]


def vectorize(text):
    return client.embeddings.create(input=[text], model=EMBEDDING_MODEL).data[0].embedding


def parse_hotel(file_name):
    """Return (hotel_type, hotel_name) from a filename like 'family_hotel_Mare Imbrium Oasis.txt'."""
    stem = file_name.removesuffix(".txt")
    lower = stem.lower()
    for prefix in ("family_hotel_", "luxury_", "hostel_"):
        if lower.startswith(prefix):
            return prefix.rstrip("_"), stem[len(prefix):]
    return None, None


def create_schema(con):
    con.execute("DROP TABLE IF EXISTS hotels")
    con.execute("DROP TABLE IF EXISTS availabilities")
    con.execute("DROP TABLE IF EXISTS space_travel_vectors")
    con.execute(
        """
        CREATE TABLE hotels (
            name TEXT PRIMARY KEY,
            location TEXT NOT NULL,
            descriptionFile TEXT NOT NULL,
            price INTEGER NOT NULL
        )
        """
    )
    con.execute(
        """
        CREATE TABLE availabilities (
            name TEXT NOT NULL,
            start TEXT NOT NULL,
            end TEXT NOT NULL
        )
        """
    )
    con.execute(
        f"""
        CREATE VIRTUAL TABLE space_travel_vectors USING vec0(
            id INTEGER PRIMARY KEY,
            name TEXT,
            chunk_id INTEGER,
            embedding float[{EMBEDDING_DIM}]
        )
        """
    )


def seed_hotels_and_vectors(con):
    for folder in sorted(os.listdir(SPACE_DIR)):
        location = LOCATION_BY_FOLDER.get(folder)
        if location is None:
            print(f"  skipping unknown folder: {folder}")
            continue
        folder_path = SPACE_DIR / folder
        for file_name in sorted(os.listdir(folder_path)):
            if not file_name.endswith(".txt") or "prompt" in file_name.lower():
                continue
            file_path = folder_path / file_name
            rel_path = str(file_path.relative_to(ROOT))

            hotel_type, hotel_name = parse_hotel(file_name)
            if hotel_type is not None:
                price = HOTEL_PRICE_BY_TYPE[hotel_type]
                con.execute(
                    "INSERT OR REPLACE INTO hotels(name, location, descriptionFile, price) VALUES (?, ?, ?, ?)",
                    (hotel_name, location, rel_path, price),
                )
                for start, end in AVAILABILITY_WINDOWS:
                    con.execute(
                        "INSERT INTO availabilities(name, start, end) VALUES (?, ?, ?)",
                        (hotel_name, start, end),
                    )
                print(f"  hotel:  {hotel_name} ({location}, {price}€/night)")

            print(f"  vector: {rel_path}")
            with open(file_path, "r") as f:
                text = f.read()
            for chunk_id, chunk in enumerate(chunker(text)):
                vector = vectorize(chunk)
                con.execute(
                    "INSERT INTO space_travel_vectors(name, chunk_id, embedding) VALUES (?, ?, ?)",
                    (rel_path, chunk_id, pack_vector(vector)),
                )


def main():
    if DB_PATH.exists():
        DB_PATH.unlink()
    con = sqlite3.connect(DB_PATH)
    con.enable_load_extension(True)
    sqlite_vec.load(con)
    con.enable_load_extension(False)

    create_schema(con)
    seed_hotels_and_vectors(con)
    con.commit()

    hotel_count = con.execute("SELECT COUNT(*) FROM hotels").fetchone()[0]
    avail_count = con.execute("SELECT COUNT(*) FROM availabilities").fetchone()[0]
    vec_count = con.execute("SELECT COUNT(*) FROM space_travel_vectors").fetchone()[0]
    print(f"\nDone. {hotel_count} hotels, {avail_count} availabilities, {vec_count} vector chunks → {DB_PATH}")
    con.close()


if __name__ == "__main__":
    main()
