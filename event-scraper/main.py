from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from declarations import Event, Base
from fhku_event_scraper import get_latest_events


engine = create_engine('sqlite:///events_db.sqlite')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

events = get_latest_events()

for event in events:
    ev = session.query(Event).filter_by(identifier=event['identifier']).first()

    if not ev:
        session.add(Event(
            name=event['name'],
            location=event['location'],
            link=event['link'],
            short=event['short'],
            date=event['date'],
            source=event['source'],
            identifier=event['identifier']
        ))

session.commit()
session.close()