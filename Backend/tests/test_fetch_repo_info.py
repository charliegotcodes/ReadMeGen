from app.services.github_client import fetch_repo_info
from app.models.repo_summary import ReadmeInfo

def test_fetch_repo_info_valid():
    url = "https://github.com/charliegotcodes/SpotifyPlaylistGeneratorPy"

    results = fetch_repo_info(url)

    assert isinstance (results, ReadmeInfo)

    assert results.repo_owner == "charliegotcodes"
    assert results.repo_name == "SpotifyPlaylistGeneratorPy"

    assert results.repo_techstack == "Python, HTML, Procfile"
