from flask import Flask, render_template, request
import requests
import os
import time

app = Flask(__name__)

#Credentials
CLIENT_ID = os.getenv('IGDB_CLIENT_ID', '') #Your IGBD Client ID
CLIENT_SECRET = os.getenv('IGDB_CLIENT_SECRET', '') #Your IGDB Client Secret

#Getting access token
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

#Requests to the IGDB API
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

#Search Games
def search_games(query, page=1, per_page=20):
    offset = (page - 1) * per_page
    query = f'search "{query}"; fields name,cover.url,summary,release_dates.human; where cover != null; limit {per_page}; offset {offset};'
    results = igdb_request('games', query)
    
    for game in results:
        if 'cover' in game and 'url' in game['cover']:
            game['cover']['url'] = game['cover']['url'].replace('t_thumb', 't_720p')
    return results


#Routes
@app.route('/')
def index():
    return render_template('index.html', title='Home')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    page = request.args.get('page', default=1, type=int)
    per_page = 20
    search_results = search_games(query, page=page, per_page=per_page)
    return render_template('search_results.html', title='Search Results', results=search_results, query=query, page=page)


@app.route('/game/<int:game_id>')
def game_detail(game_id):
    # Query game using the game_id
    query = f'fields name,cover.url,summary,genres.name,platforms.name,release_dates.human; where id = {game_id};'
    game_details = igdb_request('games', query)
    
    #Check if the API returned any data
    if not game_details:
        return render_template('error.html', message='Game not found'), 404
    
    game = game_details[0]
    return render_template('game_detail.html', title=game['name'], game=game)

@app.route('/trending')
def trending():
    # Query for recent popular games
    current_timestamp = int(time.time())
    two_years_ago = current_timestamp - (2 * 365 * 24 * 60 * 60)
    
    query = '''
    fields name,cover.url,summary,release_dates.human,rating,rating_count;
    where 
        rating_count > 50 & 
        cover != null & 
        first_release_date > {two_years_ago} & 
        first_release_date < {current_timestamp};
    sort rating desc;
    limit 20;
    '''.format(two_years_ago=two_years_ago, current_timestamp=current_timestamp)
    
    trending_games = igdb_request('games', query)
    
    for game in trending_games:
        if 'cover' in game and 'url' in game['cover']:
            game['cover']['url'] = game['cover']['url'].replace('t_thumb', 't_720p')
    
    return render_template('trending.html', title='Trending Games', games=trending_games)

@app.route('/top')
def top_games():
    query = '''
    fields name,cover.url,summary,release_dates.human,rating,rating_count;
    where 
        rating_count > 100 & 
        cover != null & 
        rating > 0;
    sort rating desc;
    limit 20;
    '''
    
    top_games = igdb_request('games', query)
    
    for game in top_games:
        if 'cover' in game and 'url' in game['cover']:
            game['cover']['url'] = game['cover']['url'].replace('t_thumb', 't_720p')
    
    return render_template('top_games.html', title='Top Rated Games', games=top_games)

if __name__ == '__main__':
    app.run(debug=True)
