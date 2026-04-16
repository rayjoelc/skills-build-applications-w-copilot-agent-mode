from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models
from pymongo import MongoClient

# Sample data for superheroes, teams, activities, leaderboard, and workouts
data = {
    "users": [
        {"name": "Clark Kent", "email": "superman@dc.com", "team": "DC"},
        {"name": "Bruce Wayne", "email": "batman@dc.com", "team": "DC"},
        {"name": "Diana Prince", "email": "wonderwoman@dc.com", "team": "DC"},
        {"name": "Tony Stark", "email": "ironman@marvel.com", "team": "Marvel"},
        {"name": "Steve Rogers", "email": "captainamerica@marvel.com", "team": "Marvel"},
        {"name": "Natasha Romanoff", "email": "blackwidow@marvel.com", "team": "Marvel"},
    ],
    "teams": [
        {"name": "Marvel"},
        {"name": "DC"},
    ],
    "activities": [
        {"user": "superman@dc.com", "activity": "Flight", "duration": 60},
        {"user": "batman@dc.com", "activity": "Martial Arts", "duration": 45},
        {"user": "ironman@marvel.com", "activity": "Engineering", "duration": 120},
    ],
    "leaderboard": [
        {"user": "superman@dc.com", "points": 1000},
        {"user": "ironman@marvel.com", "points": 950},
        {"user": "wonderwoman@dc.com", "points": 900},
    ],
    "workouts": [
        {"name": "Super Strength", "suggested_for": "DC"},
        {"name": "Tech Training", "suggested_for": "Marvel"},
    ]
}

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        # Drop collections if they exist
        for collection in ["users", "teams", "activities", "leaderboard", "workouts"]:
            db[collection].drop()

        # Insert test data
        for collection, docs in data.items():
            db[collection].insert_many(docs)

        # Ensure unique index on email for users
        db["users"].create_index([("email", 1)], unique=True)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
