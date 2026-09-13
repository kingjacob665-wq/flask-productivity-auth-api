from config import app, db
from models import User, Task
from faker import Faker
import random

fake = Faker()

with app.app_context():
    print("Clearing database...")
    Task.query.delete()
    User.query.delete()

    print("Seeding users...")
    users = []
    for _ in range(5):
        user = User(username=fake.unique.user_name())
        user.password_hash = "password123"
        users.append(user)
        db.session.add(user)

    db.session.commit()

    print("Seeding tasks...")
    for user in users:
        for _ in range(random.randint(2, 5)):
            task = Task(
                title=fake.sentence(nb_words=4),
                description=fake.sentence(nb_words=10),
                completed=random.choice([True, False]),
                user_id=user.id
            )
            db.session.add(task)

    db.session.commit()
    print("Done seeding!")
