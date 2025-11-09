"""
Example usage of the YummyAnime video player.

This example demonstrates how to integrate the player with the YummyAPI
to load and play anime episodes with all the new features:
- Rewind button (⏪) - 5 seconds backward
- Forward button (⏩) - 5 seconds forward, double-click for next episode
- Auto quality selection based on bandwidth and buffer status
"""

import asyncio
from yummyanime import YummyApi
from yummyanime.player_helper import get_video_qualities_data, prepare_player_data


async def example_load_episode():
    """
    Example: Load an episode and prepare data for the player.
    """
    # Initialize API
    api = YummyApi(x_application_token='8umoarkosg8_4ktkvmqpcuf0wun37wxu')
    
    # Example: Load episode data
    slug = 'example-anime-slug'
    episode_index = 0
    
    try:
        # Get video qualities data
        qualities_data = await get_video_qualities_data(api, slug, episode_index)
        
        # This data can be passed to the frontend player via:
        # window.loadEpisodeWithData(qualities_data, 'auto')
        
        print("Qualities data:", qualities_data)
        
        # Or get complete player data
        player_data = await prepare_player_data(api, slug, episode_index)
        print("Player data:", player_data)
        
    except Exception as e:
        print(f"Error: {e}")


async def example_with_web_server():
    """
    Example: Using the player with a web server (Flask/FastAPI).
    
    For a complete integration, you would:
    1. Serve the player.html file
    2. Create an API endpoint that calls get_video_qualities_data()
    3. Have the frontend call that endpoint to load episodes
    """
    from flask import Flask, jsonify, send_file
    import os
    
    app = Flask(__name__)
    api = YummyApi(x_application_token='8umoarkosg8_4ktkvmqpcuf0wun37wxu')
    
    @app.route('/player')
    def serve_player():
        """Serve the player HTML file."""
        player_path = os.path.join(os.path.dirname(__file__), 'player.html')
        return send_file(player_path)
    
    @app.route('/api/anime/<slug>/video/<int:episode_index>/qualities')
    async def get_qualities(slug, episode_index):
        """API endpoint to get video qualities."""
        try:
            qualities_data = await get_video_qualities_data(api, slug, episode_index)
            return jsonify(qualities_data)
        except Exception as e:
            return jsonify({'error': str(e)}), 404
    
    # Run the server
    # app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    # Run the example
    asyncio.run(example_load_episode())

