from app import db, Emoji

emojis = [
    'banana',
    'cookie',
    'hot_beverage',
    'red_heart',
    'sparkles',
    'umbrella',
]

for emoji_name in emojis:
    db.session.add(Emoji(name = emoji_name))
db.session.commit()