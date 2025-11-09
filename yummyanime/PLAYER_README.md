# YummyAnime Video Player

A feature-rich video player interface for YummyAnime episodes with adaptive quality selection, rewind/forward controls, and full accessibility support.

## Features

### 1. Rewind Button (⏪)
- **Location**: Left of the Pause button
- **Function**: Rewinds video by 5 seconds
- **Tooltip**: "⏪ Rewind 5 seconds."
- **Accessibility**: 
  - Keyboard accessible (Tab to focus, Enter/Space to activate)
  - ARIA label: "rewind 5 seconds"
  - Visible focus outline

### 2. Forward Button (⏩)
- **Location**: Right of the Pause button
- **Function**: 
  - Single click: Skips forward 5 seconds
  - Double click: Jumps to next episode
  - Long tap (>400ms): Jumps to next episode
- **Tooltip**: "⏩ Forward 5 seconds / double-click for next episode."
- **Accessibility**: 
  - Keyboard accessible (Tab to focus, Enter/Space to activate)
  - ARIA label: "skip forward 5 seconds"
  - Visible focus outline

### 3. Auto Quality Selection
- **Function**: Automatically selects optimal playback quality based on:
  - Connection speed (bandwidth test on episode start)
  - Player size and device pixel ratio
  - Buffer status (monitored every 10 seconds)
  - Connection stability (checked every 5 seconds)
- **Behavior**:
  - On episode start: Measures bandwidth (~200 KB test), selects highest quality where `bitrate < 0.7 * measured_throughput` and `height ≤ playerHeight * devicePixelRatio`
  - Every 10 seconds: If buffer < 6 seconds → switch to lower quality
  - Every 5 seconds: If connection stable for >30 seconds → switch to higher quality
- **Manual Override**: Users can manually select quality or toggle Auto mode

## Usage

### Basic Integration

1. **Serve the player HTML file** in your web application
2. **Use the Python helper** to get video qualities:

```python
from yummyanime import YummyApi
from yummyanime.player_helper import get_video_qualities_data

api = YummyApi(x_application_token='8umoarkosg8_4ktkvmqpcuf0wun37wxu')
qualities_data = await get_video_qualities_data(api, slug='anime-slug', episode_index=0)

# Pass to frontend
# In your JavaScript:
window.loadEpisodeWithData(qualities_data, 'auto')
```

### API Integration Pattern

The player follows the pattern described in requirements:

```python
# Python backend
anime = await api.anime.get(slug, need_videos=True)
video = await video.qualities(anime.response)  # This is video_kodik.qualities equivalent
```

The `player_helper.py` module provides convenient wrappers for this pattern.

### Frontend API

The player exposes two main functions:

```javascript
// Load episode via API endpoint
window.loadEpisode(apiEndpoint, slug, episodeIndex);

// Load episode with pre-loaded data
window.loadEpisodeWithData(qualitiesData, initialQuality);
```

### Next Episode Callback

To handle next episode navigation, implement:

```javascript
window.onNextEpisode = function() {
    // Navigate to next episode
    // Example: loadNextEpisode();
};
```

## File Structure

- `player.html` - Complete video player interface with all features
- `player_helper.py` - Python helper functions for API integration
- `player_example.py` - Example usage code

## Styling

The player includes:
- Modern, responsive design
- Dark theme optimized for video viewing
- Smooth transitions and hover effects
- Mobile-friendly touch controls
- Accessible focus indicators

## Browser Compatibility

- Modern browsers with HTML5 video support
- Requires ES6+ JavaScript support
- Touch events for mobile devices

## Accessibility

- Full keyboard navigation support
- ARIA labels on all interactive elements
- Visible focus outlines
- Screen reader friendly
- Tooltips for all controls

