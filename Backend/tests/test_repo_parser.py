from app.services.github_client import repo_url_parser


def test_repo_parser_url_valid():
    url = "https://github.com/charliegotcodes/SpotifyPlaylistGeneratorPy"
    owner, repo = repo_url_parser(url)

    assert owner == "charliegotcodes"
    assert repo == "SpotifyPlaylistGeneratorPy"

def test_repo_parser_url_invalid():
    url = "https://github.com/just-owner-no-repo"

    try:
        repo_url_parser(url)
        assert False, "Expected ValueError but function did not raise"
    except ValueError:
        assert True
