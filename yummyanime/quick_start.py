"""
Quick start script with your API token pre-configured.
"""

import asyncio
from yummyanime import YummyApi
from yummyanime.player_helper import get_video_qualities_data, prepare_player_data

# Your API token
API_TOKEN = '8umoarkosg8_4ktkvmqpcuf0wun37wxu'


async def load_episode(slug: str, episode_index: int = 0):
    """
    Load an episode and get video qualities data.
    
    Args:
        slug: Anime slug identifier
        episode_index: Episode index (0-based, default: 0)
    
    Returns:
        Dictionary with qualities data ready for the player
    """
    api = YummyApi(x_application_token=API_TOKEN)
    
    try:
        qualities_data = await get_video_qualities_data(api, slug, episode_index)
        return qualities_data
    except Exception as e:
        print(f"Error loading episode: {e}")
        raise


async def get_full_player_data(slug: str, episode_index: int = 0):
    """
    Get complete player data including anime info and qualities.
    
    Args:
        slug: Anime slug identifier
        episode_index: Episode index (0-based, default: 0)
    
    Returns:
        Dictionary with anime info, episode info, and qualities
    """
    api = YummyApi(x_application_token=API_TOKEN)
    
    try:
        player_data = await prepare_player_data(api, slug, episode_index)
        return player_data
    except Exception as e:
        print(f"Error getting player data: {e}")
        raise


# Example usage
if __name__ == '__main__':
    async def main():
        # Replace with your actual anime slug
        slug = 'example-anime-slug'
        
        # Get qualities data
        qualities = await load_episode(slug, episode_index=0)
        print("Qualities loaded:", list(qualities.keys()))
        
        # Or get full player data
        # player_data = await get_full_player_data(slug, episode_index=0)
        # print("Player data:", player_data)
    
    asyncio.run(main())

