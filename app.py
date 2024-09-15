from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# Client credentials
CLIENT_ID = os.getenv('IGDB_CLIENT_ID', '76w5hvlmx45sguz4wh52n19qkyy9sp')
CLIENT_SECRET = os.getenv('IGDB_CLIENT_SECRET', '5hshzpma6v75dqi5ycgdcluzaygxt2')

# Function to get access token
def get_access_token():
    url = 'https://id.twitch.tv/oauth2/token'
    params = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, params=params)
    access_token = response.json().get('access_token')
    return access_token

# Function to make requests to the IGDB API
def igdb_request(endpoint, query):
    access_token = get_access_token()
    headers = {
        'Client-ID': CLIENT_ID,
        'Authorization': f'Bearer {access_token}'
    }
    url = f'https://api.igdb.com/v4/{endpoint}'
    response = requests.post(url, headers=headers, data=query)
    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.json()}")
        return []
    return response.json()

# Search Games
def search_games(query):
    query = f'search "{query}*"; fields name,cover.url,summary; limit 10;'
    return igdb_request('games', query)

# Routes
@app.route('/')
def index():
    return render_template('index.html', title='Home')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    search_results = search_games(query)
    return render_template('search_results.html', title='Search Results', results=search_results)

@app.route('/game/<int:game_id>')
def game_detail(game_id):
    # Query the API for the specific game using the game_id
    query = f'fields name,cover.url,summary,genres.name,platforms.name,release_dates.human; where id = {game_id};'
    game_details = igdb_request('games', query)
    
    # Check if the API returned any data
    if not game_details:
        return render_template('error.html', message='Game not found'), 404
    
    game = game_details[0]  # There should be only one game with this ID
    return render_template('game_detail.html', title=game['name'], game=game)


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
