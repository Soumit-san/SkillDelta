import os
import requests
import re
from typing import List
from datetime import datetime, timedelta

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"

# 🔹 Acronym mapping
SHORT_FORM_MAP = {
    "cn": "computer networks",
    "da": "data analysis",
    "ds": "data science",
    "dsa": "data structures and algorithms",
    "os": "operating systems",
    "dbms": "database management systems",
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "nlp": "natural language processing",
    "cv": "computer vision",
    "oops": "object oriented programming",
    "frontend": "frontend web development",
    "backend": "backend web development",
    "dl": "deep learning",
    "sql": "structured query language"
}

# 🔹 In-memory cache
youtube_cache = {}

# 🔹 Cache TTL (minutes)
CACHE_TTL_MINUTES = 60


def normalize_query(query: str) -> str:
    """
    Normalize query to avoid duplicate similar calls.
    """
    return query.strip().lower()


def fetch_youtube_videos(query: str, skill_name: str = None, max_results: int = 3) -> List[dict]:

    if not YOUTUBE_API_KEY:
        print("YouTube API key missing.")
        return []

    # 🔹 Expand acronyms for query
    expanded_query = query
    for short_form, full_form in SHORT_FORM_MAP.items():
        if short_form in expanded_query.lower().split():
            expanded_query = re.sub(rf'\b{short_form}\b', full_form, expanded_query, flags=re.IGNORECASE)

    search_term = expanded_query

    # 🔹 Append skill context if provided
    if skill_name:
        expanded_skill = skill_name
        for short_form, full_form in SHORT_FORM_MAP.items():
            if short_form in expanded_skill.lower().split():
                expanded_skill = re.sub(rf'\b{short_form}\b', full_form, expanded_skill, flags=re.IGNORECASE)
                
        if expanded_skill.lower() not in search_term.lower():
            search_term = f"{expanded_skill} {search_term}"

    normalized_query = normalize_query(search_term)
    now = datetime.utcnow()

    # 🔹 Check cache
    if normalized_query in youtube_cache:
        cached_entry = youtube_cache[normalized_query]

        if cached_entry["expires"] > now:
            return cached_entry["data"]
        else:
            del youtube_cache[normalized_query]

    params = {
        "part": "snippet",
        "q": search_term,
        "type": "video",
        "maxResults": max_results,
        "order": "relevance",
        "videoEmbeddable": "true",
        "safeSearch": "moderate",
        "key": YOUTUBE_API_KEY,
    }

    try:
        response = requests.get(
            YOUTUBE_SEARCH_URL,
            params=params,
            timeout=5
        )

        if response.status_code != 200:
            print("YouTube API error:", response.status_code)
            return []

        data = response.json()
        results = []

        items = data.get("items", [])[:3]

        # 🔹 Extract unique channel IDs to fetch logos in bulk
        channel_ids = list({item.get("snippet", {}).get("channelId") for item in items if item.get("snippet", {}).get("channelId")})
        
        channel_logos = {}
        if channel_ids:
            try:
                channel_resp = requests.get(
                    "https://www.googleapis.com/youtube/v3/channels",
                    params={
                        "part": "snippet",
                        "id": ",".join(channel_ids),
                        "key": YOUTUBE_API_KEY
                    },
                    timeout=5
                )
                if channel_resp.status_code == 200:
                    for c_item in channel_resp.json().get("items", []):
                        channel_logos[c_item["id"]] = c_item.get("snippet", {}).get("thumbnails", {}).get("default", {}).get("url")
            except Exception as e:
                print("Could not fetch channel logos:", e)

        for item in items:
            video_id = item.get("id", {}).get("videoId")
            snippet = item.get("snippet", {})

            if not video_id:
                continue

            results.append({
                "title": snippet.get("title"),
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "channel": snippet.get("channelTitle"),
                "channel_logo": channel_logos.get(snippet.get("channelId")),
                "type": "video"
            })

        # 🔹 Hard safety cap (never exceed 3)
        results = results[:3]

        # 🔹 Store in cache
        youtube_cache[normalized_query] = {
            "data": results,
            "expires": now + timedelta(minutes=CACHE_TTL_MINUTES)
        }

        return results

    except Exception as e:
        print("YouTube fetch exception:", e)
        return []