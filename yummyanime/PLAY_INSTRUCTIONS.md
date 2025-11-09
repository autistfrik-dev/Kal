# How to Play the Video Player

## Quick Start

1. **Start the server:**
   ```bash
   cd "c:\Users\Bogda\AppData\Local\Programs\Python\Python310\Lib\site-packages\yummyanime"
   python simple_server.py
   ```

2. **Open your browser:**
   - Navigate to: `http://localhost:5000`
   - You should see the video player interface

3. **Load an episode:**
   - Open the browser console (F12)
   - Run this command (replace with actual anime slug):
   ```javascript
   window.loadEpisode('http://localhost:5000/api', 'your-anime-slug', 0)
   ```

## Alternative: Direct API Call

You can also load episode data directly:

```javascript
// In browser console
fetch('http://localhost:5000/api/anime/your-anime-slug/video/0/qualities')
  .then(r => r.json())
  .then(data => window.loadEpisodeWithData(data, 'auto'))
```

## Features Available

- ⏪ **Rewind Button**: Click to rewind 5 seconds
- ⏩ **Forward Button**: 
  - Single click: Skip 5 seconds forward
  - Double click: Go to next episode
- **Auto Quality**: Automatically adjusts quality based on connection
- **Manual Quality**: Click quality buttons to manually select

## API Endpoints

- `GET /` - Player interface
- `GET /api/anime/<slug>/video/<episode_index>/qualities` - Get video qualities
- `GET /api/anime/<slug>/player-data/<episode_index>` - Get complete player data
- `GET /api/search?q=<query>` - Search for anime

## Troubleshooting

- **Server won't start**: Make sure port 5000 is not in use
- **Can't load episode**: Check that the anime slug is correct
- **No video**: Verify your API token is valid and the episode exists

