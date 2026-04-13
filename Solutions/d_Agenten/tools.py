"""Tools available to the agent. All implementations are pre-written so the
exercises can focus on the agent loop itself."""
import sqlite3
import struct
from datetime import datetime
from pathlib import Path

import sqlite_vec
from openai import AzureOpenAI

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "travel.db"

con = sqlite3.connect(DB_PATH)
con.enable_load_extension(True)
sqlite_vec.load(con)
con.enable_load_extension(False)
cur = con.cursor()

client = AzureOpenAI()


def calculate_duration(start_date_string, end_date_string):
    start_date = datetime.strptime(start_date_string, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_string, "%Y-%m-%d")
    return (end_date - start_date).days


def calculate_hotel_cost(start_date, end_date, price):
    return calculate_duration(start_date, end_date) * price


def list_hotels(location):
    rows = cur.execute("SELECT name FROM hotels WHERE location = ?", (location,)).fetchall()
    return ", ".join(row[0] for row in rows)


def get_hotel_availabilities(hotel_name):
    rows = cur.execute(
        "SELECT start, end FROM availabilities WHERE name = ?", (hotel_name,)
    ).fetchall()
    if not rows:
        raise Exception(f"Hotel '{hotel_name}' does not exist")
    return rows


def give_hotel_information(hotel_name):
    details = cur.execute(
        "SELECT descriptionFile, price FROM hotels WHERE name = ?", (hotel_name,)
    ).fetchone()
    if details is None:
        raise Exception(f"Hotel '{hotel_name}' does not exist")
    availabilities = get_hotel_availabilities(hotel_name)
    availability_string = " and ".join(f"from {start} to {end}" for start, end in availabilities)
    return f"price per night: {details[1]}€, availabilities: {availability_string}"


def book_hotel(hotel_name, check_in, check_out):
    check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
    check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
    if check_in_date > check_out_date:
        raise Exception("Check-in date is after check-out date")

    availabilities = get_hotel_availabilities(hotel_name)
    is_available = any(
        datetime.strptime(start, "%Y-%m-%d") <= check_in_date
        and datetime.strptime(end, "%Y-%m-%d") >= check_out_date
        for start, end in availabilities
    )
    if not is_available:
        raise Exception("No room available for that date range")

    price = cur.execute("SELECT price FROM hotels WHERE name = ?", (hotel_name,)).fetchone()[0]
    cost = calculate_hotel_cost(check_in, check_out, price)
    return f"Hotel {hotel_name} booked from {check_in} to {check_out} for {cost}€"


def vectorize_user_request(user_request):
    embedding = client.embeddings.create(
        input=[user_request], model="text-embedding-3-large"
    ).data[0].embedding
    return struct.pack(f"{len(embedding)}f", *embedding)


def give_tourist_information_space(user_request):
    """RAG against travel.db: returns text from the closest matching files."""
    packed = vectorize_user_request(user_request)
    rows = con.execute(
        """
        SELECT name FROM space_travel_vectors
        WHERE embedding MATCH ?
        ORDER BY distance
        LIMIT 5
        """,
        (packed,),
    ).fetchall()
    seen = set()
    parts = []
    for (file_path,) in rows:
        if file_path in seen:
            continue
        seen.add(file_path)
        with open(PROJECT_ROOT / file_path, "r") as f:
            parts.append(f.read())
    return "\n\n".join(parts)
