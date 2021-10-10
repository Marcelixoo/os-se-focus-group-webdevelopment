from flask import Flask

app = Flask(__name__)

app.config['FLASK_APP'] = 'app'
app.config['FLASK_ENV'] = 'development'

emoji_size = 512
emojis = [
    'banana',
    'cookie',
    'hot_beverage',
    'red_heart',
    'sparkles',
    'umbrella',
]


@app.route('/')
def index():
    def markup(emoji):
        return f'<li><a href="/emojis/{emoji}">{emoji}</a></li>'
    list_of_emojis = [markup(emoji) for emoji in emojis]
    return f'''
        <h1>My favorite emojis</h1>
        <ul>{''.join(list_of_emojis)}</ul>
    '''


@app.route('/emojis/<name>')
def emoji(name):
    return f'''
        <h1>My favorite emojis</h1>
        <img
            src=https://emojiapi.dev/api/v1/{name}/{emoji_size}.png
            alt={name}
            style="max-height:200px; max-width:200px;" />
        <div>
            <a href="/">Back</a>
        </div>
    '''
