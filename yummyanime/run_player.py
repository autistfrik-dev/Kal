"""
Run the YummyAnime video player server.

This script starts a web server that serves the player interface
and provides API endpoints for loading episodes.
"""

import asyncio
import os
from pathlib import Path
from flask import Flask, jsonify, send_file, request
from flask_cors import CORS
from yummyanime import YummyApi
from yummyanime.player_helper import get_video_qualities_data, prepare_player_data

# Your API token
API_TOKEN = '8umoarkosg8_4ktkvmqpcuf0wun37wxu'

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Initialize API
api = YummyApi(x_application_token=API_TOKEN)

# Get the directory where this file is located
BASE_DIR = Path(__file__).parent


@app.route('/')
def index():
    """Serve the player HTML file."""
    player_path = BASE_DIR / 'player.html'
    return send_file(str(player_path))


@app.route('/api/anime/<slug>/video/<int:episode_index>/qualities')
def get_qualities(slug, episode_index):
    """API endpoint to get video qualities for an episode."""
    async def fetch_qualities():
        try:
            qualities_data = await get_video_qualities_data(api, slug, episode_index)
            return jsonify(qualities_data)
        except Exception as e:
            return jsonify({'error': str(e)}), 404
    
    # Run async function
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(fetch_qualities())
    finally:
        loop.close()


@app.route('/api/anime/<slug>/player-data/<int:episode_index>')
def get_player_data(slug, episode_index):
    """API endpoint to get complete player data."""
    async def fetch_data():
        try:
            player_data = await prepare_player_data(api, slug, episode_index)
            return jsonify(player_data)
        except Exception as e:
            return jsonify({'error': str(e)}), 404
    
    # Run async function
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(fetch_data())
    finally:
        loop.close()


@app.route('/api/search')
def search_anime():
    """Search for anime by query."""
    query = request.args.get('q', '')
    if not query:
        return jsonify({'error': 'Query parameter "q" is required'}), 400
    
    async def fetch_search():
        try:
            result = await api.anime.search(query, limit=10)
            return jsonify({
                'response': result.response,
                'timings': [{'name': t.name, 'duration': t.duration} for t in result.timings]
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # Run async function
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(fetch_search())
    finally:
        loop.close()


if __name__ == '__main__':
    print("=" * 60)
    print("YummyAnime Video Player Server")
    print("=" * 60)
    print(f"\nServer starting...")
    print(f"API Token: {API_TOKEN[:20]}...")
    print(f"\nOpen your browser and navigate to:")
    print(f"  http://localhost:5000")
    print(f"\nTo load an episode, use the JavaScript console:")
    print(f"  window.loadEpisode('http://localhost:5000/api', 'anime-slug', 0)")
    print(f"\nOr use the direct API endpoint:")
    print(f"  http://localhost:5000/api/anime/<slug>/video/<episode_index>/qualities")
    print("\n" + "=" * 60 + "\n")
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)

