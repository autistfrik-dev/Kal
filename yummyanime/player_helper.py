"""
Helper module for integrating the YummyAnime video player with the API.
This module provides functions to prepare video data for the frontend player.
"""

import json
from typing import Optional, Dict, Any

from .api import YummyApi
from .structs.anime import IOneAnimeJson
from .structs.video import IAnimeVideo


async def get_video_qualities_data(api: YummyApi, slug: str, episode_index: int) -> Dict[str, Any]:
    """
    Retrieve video qualities data for a specific episode.
    
    This function follows the pattern described in the requirements:
    - anime = await api.anime.get(slug, need_videos=True)
    - video = await video.qualities(anime.response)
    
    Args:
        api: YummyApi instance
        slug: Anime slug identifier
        episode_index: Index of the episode (0-based)
        
    Returns:
        Dictionary containing quality data in format suitable for the frontend player
    """
    # Get anime data with videos
    anime_response = await api.anime.get(slug, need_videos=True)
    anime: IOneAnimeJson = anime_response.response
    
    if not anime.videos or episode_index >= len(anime.videos):
        raise ValueError(f"Episode index {episode_index} not found")
    
    video: IAnimeVideo = anime.videos[episode_index]
    
    # Get video qualities (this is the video_kodik.qualities equivalent)
    qualities = await video.qualities(anime)
    
    # Convert to JSON-serializable format
    qualities_data = {
        'p240': {
            'url': qualities.p240.url,
            'ref': qualities.p240.ref
        } if qualities.p240 else None,
        'p360': {
            'url': qualities.p360.url,
            'ref': qualities.p360.ref
        } if qualities.p360 else None,
        'p480': {
            'url': qualities.p480.url,
            'ref': qualities.p480.ref
        } if qualities.p480 else None,
        'p720': {
            'url': qualities.p720.url,
            'ref': qualities.p720.ref
        } if qualities.p720 else None,
        'p1080': {
            'url': qualities.p1080.url,
            'ref': qualities.p1080.ref
        } if qualities.p1080 else None,
    }
    
    return qualities_data


def qualities_to_json(qualities_data: Dict[str, Any]) -> str:
    """
    Convert qualities data to JSON string for frontend consumption.
    
    Args:
        qualities_data: Dictionary from get_video_qualities_data()
        
    Returns:
        JSON string representation
    """
    return json.dumps(qualities_data)


async def prepare_player_data(api: YummyApi, slug: str, episode_index: int) -> Dict[str, Any]:
    """
    Prepare complete player data including anime info and video qualities.
    
    Args:
        api: YummyApi instance
        slug: Anime slug identifier
        episode_index: Index of the episode (0-based)
        
    Returns:
        Dictionary with anime info and qualities data
    """
    anime_response = await api.anime.get(slug, need_videos=True)
    anime: IOneAnimeJson = anime_response.response
    
    if not anime.videos or episode_index >= len(anime.videos):
        raise ValueError(f"Episode index {episode_index} not found")
    
    video: IAnimeVideo = anime.videos[episode_index]
    qualities = await video.qualities(anime)
    
    qualities_data = {
        'p240': {'url': qualities.p240.url, 'ref': qualities.p240.ref} if qualities.p240 else None,
        'p360': {'url': qualities.p360.url, 'ref': qualities.p360.ref} if qualities.p360 else None,
        'p480': {'url': qualities.p480.url, 'ref': qualities.p480.ref} if qualities.p480 else None,
        'p720': {'url': qualities.p720.url, 'ref': qualities.p720.ref} if qualities.p720 else None,
        'p1080': {'url': qualities.p1080.url, 'ref': qualities.p1080.ref} if qualities.p1080 else None,
    }
    
    return {
        'anime': {
            'title': anime.title,
            'anime_url': anime.anime_url,
            'slug': slug
        },
        'episode': {
            'index': episode_index,
            'number': video.number,
            'video_id': video.video_id
        },
        'qualities': qualities_data
    }

