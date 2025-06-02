""" 
Dummy script to pre-populate the cards collection in MongoDB. Provided its not persistent of course..
"""
from pymongo import MongoClient
import os

mongo_address = os.getenv("MONGO_ADDR")

client = MongoClient(mongo_address)
db = client.get_database("deckbuilder")

# Should I use the DB models? The database is supposed to be managed by smth else so at this level we are making our models match this
# No
cards = [
    {
        "name":"Spider-Man",
        "cost":2,
        "power":4,
        "text":"On reveal: Move to another location and bring an opponent's card with you.",
        "keywords":["move", "on_reveal"]
    },
    {
        "name":"Iron Man",
        "cost":5,
        "power":0,
        "text":"Ongoing: Your power here is doubled.",
        "keywords":["ongoing"]
    },
    {
        "name":"The Thing",
        "cost":4,
        "power":5,
        "text":"It's clobberin' time.",
        "keywords":[]
    },
    {
        "name":"Magneto",
        "cost":6,
        "power":12,
        "text":"On reveal: Move enemy 3-cost and 4-cost cards to this location",
        "keywords":["move", "on_reveal"]
    },
    {
        "name":"Morbius",
        "cost":2,
        "power":0,
        "text":"Ongoing: Has +2 power for each card you discarded this game.",
        "keywords":["ongoing", "discard"]
    },
    {
        "name":"Human Torch",
        "cost":1,
        "power":2,
        "text":"Every time this moves, double it's power.",
        "keywords":["move"]
    },
    {
        "name":"Silver Sable",
        "cost":1,
        "power":0,
        "text":"On reveal: Drain 2 power from the top card of the opponent's deck.",
        "keywords":["on_reveal"]
    },
    {
        "name":"Hazmat",
        "cost":3,
        "power":3,
        "text":"On reveal: Remove 1 power from all other cards.",
        "keywords":["on_reveal"]
    }
]

db.get_collection("cards").insert_many(cards)