import os
import requests
from urllib.parse import urlparse
from app.models.repo_summary import ReadmeInfo
from typing import Tuple 
from dotenv import load_dotenv

load_dotenv()

GITHUB_API_BASE = "https://api.github.com"

def repo_url_parser(repo_url: str) -> Tuple[str, str]:
    """ 
        Given a URL to a github repo it seperates and returns the:
        (repo_name, repo_owner)

        Ex: https://github.com/charliegotcodes/SpotifyPlaylistGeneratorPy
        => (charliegotcodes, SpotifyPlaylistGeneratorPy)

    """

    parsed = urlparse(repo_url)
    parts = parsed.path.split('/')[1:]
    print(parts)

    if (len(parts) < 2):
        raise ValueError(f"Invalid GitHub repo URL: {repo_url}")
    
    repo_owner, repo_name = parts[0], parts[1]
    return repo_owner, repo_name



def fetch_repo_info(url: str) -> ReadmeInfo:
    """
        Utilizes the repo_url and github's API to get relevant information readily available
        for readme generation such as: 
            repo_url, repo_owner, repo_name, repo_techstack
    """
    owner, name = repo_url_parser(repo_url=url)

    token = os.getenv("GITHUB_TOKEN")
    headers = {"Accept": "application/vnd.github+json"}

    if token: headers["Authorization"] = f"Bearer {token}"

    # Utilized to retrieve possible description if available
    repo_resp = requests.get(f"{GITHUB_API_BASE}/repos/{owner}/{name}", headers=headers, timeout=10)
    repo_data = repo_resp.json()

    # Utilized to discover possible techstack according to github's api response
    langs_resp = requests.get( repo_data["languages_url"], headers=headers, timeout=10 )

    languages = list(langs_resp.json().keys()) 
    languages_str = ", ".join(languages) if languages else "Not detected"
    repo_langs = languages_str

    return ReadmeInfo(
        repo_url = url,
        repo_name = name,
        repo_owner = owner,
        repo_languages = repo_langs,
        repo_summary = repo_data.get("description") or "No description provided."
    )
