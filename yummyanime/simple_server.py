"""
Simple HTTP server to run the player (no Flask required).
Uses Python's built-in http.server.
"""

import asyncio
import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import threading

from yummyanime import YummyApi
from yummyanime.player_helper import get_video_qualities_data, prepare_player_data

# Your API token
API_TOKEN = '8umoarkosg8_4ktkvmqpcuf0wun37wxu'

# Initialize API
api = YummyApi(x_application_token=API_TOKEN)

# Get the directory where this file is located
BASE_DIR = Path(__file__).parent


class PlayerHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the player server."""
    
    def do_GET(self):
        """Handle GET requests."""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Serve player HTML
        if path == '/' or path == '/player.html':
            self.serve_player()
        
        # API endpoint: get qualities
        elif path.startswith('/api/anime/') and '/video/' in path and '/qualities' in path:
            self.serve_qualities(path)
        
        # API endpoint: get player data
        elif path.startswith('/api/anime/') and '/player-data/' in path:
            self.serve_player_data(path)
        
        # API endpoint: search
        elif path == '/api/search':
            self.serve_search(parsed_path.query)
        
        else:
            self.send_error(404, "Not Found")
    
    def serve_player(self):
        """Serve the player HTML file."""
        player_path = BASE_DIR / 'player.html'
        try:
            with open(player_path, 'rb') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404, "Player file not found")
    
    def serve_qualities(self, path):
        """Serve video qualities data."""
        # Parse path: /api/anime/<slug>/video/<episode_index>/qualities
        parts = path.split('/')
        try:
            slug_index = parts.index('anime') + 1
            video_index = parts.index('video') + 1
            slug = parts[slug_index]
            episode_index = int(parts[video_index])
            
            # Run async function
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                qualities_data = loop.run_until_complete(
                    get_video_qualities_data(api, slug, episode_index)
                )
                self.send_json_response(qualities_data)
            except Exception as e:
                self.send_json_response({'error': str(e)}, status=404)
            finally:
                loop.close()
        except (ValueError, IndexError) as e:
            self.send_json_response({'error': f'Invalid path: {e}'}, status=400)
    
    def serve_player_data(self, path):
        """Serve complete player data."""
        # Parse path: /api/anime/<slug>/player-data/<episode_index>
        parts = path.split('/')
        try:
            slug_index = parts.index('anime') + 1
            data_index = parts.index('player-data') + 1
            slug = parts[slug_index]
            episode_index = int(parts[data_index])
            
            # Run async function
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                player_data = loop.run_until_complete(
                    prepare_player_data(api, slug, episode_index)
                )
                self.send_json_response(player_data)
            except Exception as e:
                self.send_json_response({'error': str(e)}, status=404)
            finally:
                loop.close()
        except (ValueError, IndexError) as e:
            self.send_json_response({'error': f'Invalid path: {e}'}, status=400)
    
    def serve_search(self, query_string):
        """Serve search results."""
        params = parse_qs(query_string)
        query = params.get('q', [''])[0]
        
        if not query:
            self.send_json_response({'error': 'Query parameter "q" is required'}, status=400)
            return
        
        # Run async function
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(api.anime.search(query, limit=10))
            response_data = {
                'response': result.response,
                'timings': [{'name': t.name, 'duration': t.duration} for t in result.timings]
            }
            self.send_json_response(response_data)
        except Exception as e:
            self.send_json_response({'error': str(e)}, status=500)
        finally:
            loop.close()
    
    def send_json_response(self, data, status=200):
        """Send JSON response."""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, default=str).encode('utf-8'))
    
    def log_message(self, format, *args):
        """Override to customize logging."""
        print(f"[{self.address_string()}] {format % args}")


def run_server(port=5000):
    """Run the HTTP server."""
    server_address = ('', port)
    httpd = HTTPServer(server_address, PlayerHandler)
    
    print("=" * 60)
    print("YummyAnime Video Player Server")
    print("=" * 60)
    print(f"\nServer starting on port {port}...")
    print(f"API Token: {API_TOKEN[:20]}...")
    print(f"\nOpen your browser and navigate to:")
    print(f"  http://localhost:{port}")
    print(f"\nTo load an episode, open browser console and run:")
    print(f"  window.loadEpisode('http://localhost:{port}/api', 'anime-slug', 0)")
    print(f"\nOr use the direct API endpoint:")
    print(f"  http://localhost:{port}/api/anime/<slug>/video/<episode_index>/qualities")
    print("\n" + "=" * 60)
    print("Press Ctrl+C to stop the server\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
        httpd.shutdown()


if __name__ == '__main__':
    run_server(port=5000)

