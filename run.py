from app import app, db
from faker import Faker
from app.models import Fiction, Author

fake = Faker()


with app.app_context():
    # Generate 10 fake authors
    for i in range(100):
        author = Author(
            name=fake.name(),
            birth_year=fake.random_int(min=1900, max=2023),
            author_page=fake.url(),
            about=fake.text(),
            view=fake.random_int(min=0, max=100000),
            email=fake.email(),
            img=fake.image_url(),
            fiction_count=fake.random_int(min=1, max=50)
        )
        db.session.add(author)

    db.session.commit()
    # Generate 10 fake fictions
    for i in range(100):
        fiction = Fiction(
            name=fake.sentence(),
            status=fake.word(),
            view=fake.random_int(min=0, max=100000),
            desc=fake.text(),
            cover=fake.image_url(),
            publish_year=fake.random_int(min=1900, max=2023),
            page_count=fake.random_int(min=50, max=1000),
            author_id=fake.random_int(min=1, max=100),
            tiki_link=fake.url(),
            mediafire_link=fake.url(),
            slug=fake.slug(),
            version=fake.random_int(min=1, max=100),
            short_desc=fake.sentence(),
            tag=fake.word()
        )
        db.session.add(fiction)

    db.session.commit()