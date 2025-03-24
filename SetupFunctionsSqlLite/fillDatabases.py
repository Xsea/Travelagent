import sqlite3
from datetime import datetime

con = sqlite3.connect("../travel.db")
cur = con.cursor()

# cur.execute("""
#     INSERT INTO hotels (name, location, descriptionFile, price) VALUES
#         ('MoonBase Hostel', 'Luna', 'hostel_armstrong_heights', 35),
#         ('Lunar Lodge', 'Luna', 'hostel_new_tranquility_city', 30),
#         ('Lunar Family Resort', 'Luna', 'family_hotel_Mare Imbrium Oasis', 80),
#         ('Serenity Family Hotel', 'Luna', 'family_hotel_Mare Serenitatis Resort', 95),
#         ('The Celestial Haven', 'Luna', 'luxury_Copernicus Metropolis', 200),
#         ('Hellas Basin Family Retreat', 'Mars', 'family_hotel_Hellas Basin Haven', 100),
#         ('Valles Marineris Family Resort', 'Mars', 'family_hotel_Valles Marineris Metropolis', 105),
#         ('Red Rover Hostel', 'Mars', 'hostel_Ares Domes', 35),
#         ('Red Horizon Hostel', 'Mars', 'hostel_Arsia Prime', 40),
#         ('The Celestial Garden', 'Mars', 'luxury_Cydonia Heights', 180),
#         ('The Olympus Pinnacle', 'Mars', 'luxury_New Olympus City', 220),
#         ('Starlight Family Resort', 'Massage', 'family_hotel_Elysium Haven', 100),
#         ('Star Haven Hostel', 'Massage', 'hostel_Akycha Prime', 25),
#         ('Celestial Haven Hotel', 'Massage', 'hotel Nova Arcadia', 250),
#         ('The Xenon Palace', 'Massage', 'hotel_Xenonopolis', 130)
# """)

cur.execute("INSERT INTO availabilities VALUES (?, ?, ?)", ('MoonBase Hostel', datetime(year=2026, month=1, day=1), datetime(year=2026, month=3, day=4)))
cur.execute("INSERT INTO availabilities VALUES (?, ?, ?)", ('MoonBase Hostel', datetime(year=2026, month=5, day=10), datetime(year=2026, month=8, day=14)))
cur.execute("INSERT INTO availabilities VALUES (?, ?, ?)", ('MoonBase Hostel', datetime(year=2026, month=10, day=28), datetime(year=2026, month=12, day=28)))
cur.execute("INSERT INTO availabilities VALUES (?, ?, ?)", ('Lunar Lodge', datetime(year=2026, month=2, day=2), datetime(year=2026, month=3, day=13)))
cur.execute("INSERT INTO availabilities VALUES (?, ?, ?)", ('Lunar Lodge', datetime(year=2026, month=4, day=5), datetime(year=2026, month=5, day=28)))
cur.execute("INSERT INTO availabilities VALUES (?, ?, ?)", ('Lunar Lodge', datetime(year=2026, month=10, day=12), datetime(year=2026, month=12, day=31)))
cur.execute("INSERT INTO availabilities VALUES (?, ?, ?)", ('Lunar Family Resort', datetime(year=2026, month=1, day=1), datetime(year=2026, month=1, day=28)))
cur.execute("INSERT INTO availabilities VALUES (?, ?, ?)", ('Lunar Family Resort', datetime(year=2026, month=10, day=1), datetime(year=2026, month=12, day=31)))
cur.execute("INSERT INTO availabilities VALUES (?, ?, ?)", ('Serenity Family Hotel', datetime(year=2026, month=1, day=18), datetime(year=2026, month=3, day=10)))
cur.execute("INSERT INTO availabilities VALUES (?, ?, ?)", ('Serenity Family Hotel', datetime(year=2026, month=5, day=17), datetime(year=2026, month=8, day=23)))
cur.execute("INSERT INTO availabilities VALUES (?, ?, ?)", ('Serenity Family Hotel', datetime(year=2026, month=9, day=20), datetime(year=2026, month=12, day=23)))
cur.execute("INSERT INTO availabilities VALUES (?, ?, ?)", ('The Celestial Haven', datetime(year=2026, month=3, day=2), datetime(year=2026, month=5, day=4)))
cur.execute("INSERT INTO availabilities VALUES (?, ?, ?)", ('The Celestial Haven', datetime(year=2026, month=7, day=1), datetime(year=2026, month=9, day=4)))
cur.execute("INSERT INTO availabilities VALUES (?, ?, ?)", ('The Celestial Haven', datetime(year=2026, month=11, day=1), datetime(year=2026, month=12, day=31)))
cur.execute("INSERT INTO availabilities VALUES (?, ?, ?)", ('Hellas Basin Family Retreat', datetime(year=2026, month=1, day=15), datetime(year=2026, month=3, day=18)))
cur.execute("INSERT INTO availabilities VALUES (?, ?, ?)", ('Hellas Basin Family Retreat', datetime(year=2026, month=5, day=1), datetime(year=2026, month=6, day=30)))
cur.execute("INSERT INTO availabilities VALUES (?, ?, ?)", ('Hellas Basin Family Retreat', datetime(year=2026, month=9, day=1), datetime(year=2026, month=11, day=28)))
cur.execute("INSERT INTO availabilities VALUES (?, ?, ?)", ('Valles Marineris Family Resort', datetime(year=2026, month=2, day=1), datetime(year=2026, month=4, day=4)))
cur.execute("INSERT INTO availabilities VALUES (?, ?, ?)", ('Valles Marineris Family Resort', datetime(year=2026, month=4, day=8), datetime(year=2026, month=8, day=4)))
cur.execute("INSERT INTO availabilities VALUES (?, ?, ?)", ('Valles Marineris Family Resort', datetime(year=2026, month=8, day=10), datetime(year=2026, month=10, day=4)))
cur.execute("INSERT INTO availabilities VALUES (?, ?, ?)", ('Red Rover Hostel', datetime(year=2026, month=1, day=1), datetime(year=2026, month=1, day=15)))
cur.execute("INSERT INTO availabilities VALUES (?, ?, ?)", ('Red Rover Hostel', datetime(year=2026, month=1, day=28), datetime(year=2026, month=8, day=29)))
cur.execute("INSERT INTO availabilities VALUES (?, ?, ?)", ('Red Rover Hostel', datetime(year=2026, month=10, day=14), datetime(year=2026, month=12, day=4)))
cur.execute("INSERT INTO availabilities VALUES (?, ?, ?)", ('Red Horizon Hostel', datetime(year=2026, month=1, day=1), datetime(year=2026, month=3, day=4)))
cur.execute("INSERT INTO availabilities VALUES (?, ?, ?)", ('Red Horizon Hostel', datetime(year=2026, month=5, day=10), datetime(year=2026, month=8, day=14)))
cur.execute("INSERT INTO availabilities VALUES (?, ?, ?)", ('Red Horizon Hostel', datetime(year=2026, month=10, day=28), datetime(year=2026, month=12, day=28)))
cur.execute("INSERT INTO availabilities VALUES (?, ?, ?)", ('The Celestial Garden', datetime(year=2026, month=2, day=2), datetime(year=2026, month=3, day=13)))
cur.execute("INSERT INTO availabilities VALUES (?, ?, ?)", ('The Celestial Garden', datetime(year=2026, month=4, day=5), datetime(year=2026, month=5, day=28)))
cur.execute("INSERT INTO availabilities VALUES (?, ?, ?)", ('The Celestial Garden', datetime(year=2026, month=10, day=12), datetime(year=2026, month=12, day=31)))
cur.execute("INSERT INTO availabilities VALUES (?, ?, ?)", ('The Olympus Pinnacle', datetime(year=2026, month=1, day=1), datetime(year=2026, month=3, day=4)))
cur.execute("INSERT INTO availabilities VALUES (?, ?, ?)", ('The Olympus Pinnacle', datetime(year=2026, month=1, day=1), datetime(year=2026, month=3, day=4)))
cur.execute("INSERT INTO availabilities VALUES (?, ?, ?)", ('The Olympus Pinnacle', datetime(year=2026, month=1, day=1), datetime(year=2026, month=3, day=4)))
cur.execute("INSERT INTO availabilities VALUES (?, ?, ?)", ('Starlight Family Resort', datetime(year=2026, month=1, day=18), datetime(year=2026, month=3, day=10)))
cur.execute("INSERT INTO availabilities VALUES (?, ?, ?)", ('Starlight Family Resort', datetime(year=2026, month=5, day=17), datetime(year=2026, month=8, day=23)))
cur.execute("INSERT INTO availabilities VALUES (?, ?, ?)", ('Starlight Family Resort', datetime(year=2026, month=9, day=20), datetime(year=2026, month=12, day=23)))
cur.execute("INSERT INTO availabilities VALUES (?, ?, ?)", ('Star Haven Hostel', datetime(year=2026, month=3, day=2), datetime(year=2026, month=5, day=4)))
cur.execute("INSERT INTO availabilities VALUES (?, ?, ?)", ('Star Haven Hostel', datetime(year=2026, month=7, day=1), datetime(year=2026, month=9, day=4)))
cur.execute("INSERT INTO availabilities VALUES (?, ?, ?)", ('Star Haven Hostel', datetime(year=2026, month=11, day=1), datetime(year=2026, month=12, day=31)))
cur.execute("INSERT INTO availabilities VALUES (?, ?, ?)", ('Celestial Haven Hotel', datetime(year=2026, month=1, day=15), datetime(year=2026, month=3, day=18)))
cur.execute("INSERT INTO availabilities VALUES (?, ?, ?)", ('Celestial Haven Hotel', datetime(year=2026, month=5, day=1), datetime(year=2026, month=6, day=30)))
cur.execute("INSERT INTO availabilities VALUES (?, ?, ?)", ('Celestial Haven Hotel', datetime(year=2026, month=9, day=1), datetime(year=2026, month=11, day=28)))
cur.execute("INSERT INTO availabilities VALUES (?, ?, ?)", ('The Xenon Palace', datetime(year=2026, month=2, day=1), datetime(year=2026, month=4, day=4)))
cur.execute("INSERT INTO availabilities VALUES (?, ?, ?)", ('The Xenon Palace', datetime(year=2026, month=4, day=8), datetime(year=2026, month=8, day=4)))
cur.execute("INSERT INTO availabilities VALUES (?, ?, ?)", ('The Xenon Palace', datetime(year=2026, month=8, day=10), datetime(year=2026, month=10, day=4)))
con.commit()