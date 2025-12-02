import os
import requests
from urllib.parse import urlparse
from app.models.repo_summary import ReadmeInfo
from typing import Tuple 
from dotenv import load_dotenv

load_dotenv()

GITHUB_API_BASE = "https://api.github.com"
headers = {"Accept": "application/vnd.github+json"}




def contents_cleaner(contents_data:list):
    """ 
        Cleans the list of dictionaries of the files that are unecessary
        to the function of the github repo. Then returns the cleaned list of dictionaries.
    """
    final_data = []
    for item in contents_data:
        if item['name'] not in ['.DS_Store', '.cache', "__pycache__", '*.pyc', '*.pyo', '.pytest_cache/', '.mypy_cache/','.venv/',  'env/', '.gitignore', '.git/', '*.png', '*.jpg',' *.jpeg', '*.mp4']:
            final_data.append(item)
    
    print(final_data)
    return final_data

# This files goal is to build the repo_structure that will be used in the generated ReadMe.md
def list_repo_contents(owner, repo, path: str = ""):
    """
        Returns a list of dictionaries for the contents for the repo at the specified pathing.
    """
    token = os.getenv("GITHUB_TOKEN")

    if token: headers["Authorization"] = f"Bearer {token}"

    # Utilized to retrieve possible description if available
    repo_resp = requests.get(f"{GITHUB_API_BASE}/repos/{owner}/{repo}/contents/{path}", headers=headers, timeout=10)

    if repo_resp.status_code != 200:
        return []
    
    data = contents_cleaner(repo_resp.json())
              
    if isinstance(data, dict):
        return [data]
    

    return data

def create_tree(node, prefix: str="") :
    """
        Recursively converts a directory tree node into a list of display lines.
        Generates ASCII-style branches and indentation to visually represent the project structure.
    """

    lines: list[str] = []

    children = node.get("children", [])
    total = len(children)

    for idx, child in enumerate(children):
        is_last = (idx == total - 1)
        branch = "└──" if is_last else "├── "

        if child['type'] == "file":
            lines.append(f"{prefix}{branch}{child['name']}")
        else:
            lines.append(f"{prefix}{branch}{child['name']}/")
            extension = "     " if is_last else "|     "
            lines.extend(create_tree(child, prefix + extension))

    return lines



def repo_structure_creator(owner, repo, path: str = ""):
    """
        Performs a DFS traversal of the GitHub repository starting at `path`.
        Builds and returns a nested dictionary representing the directory tree:
        {
            "name": <folder>,
            "type": "dir",
            "children": [...]
        }
    """
    if path == "":
        node_name = repo
    else:
        node_name = path.split("/")[-1]
    
    node = {
        "name": node_name,
        "type": "dir",
        "children": [],
    }

    items = list_repo_contents(owner,repo, path)

    # Sorting

    dirs = [it for it in items if it['type'] == 'dir']
    files = [it for it in items if it['type'] == 'file']

    #DFS into directories

    for d in dirs: 
        child_path = d['path']
        child_node = repo_structure_creator(owner, repo, child_path)
        node["children"].append(child_node)
    
    for f in files:
        node["children"].append({
            "name": f['name'],
            'type': "file"
        })
    

    return node

def generate_project_structure(owner, repo):
    tree = repo_structure_creator(owner, repo)
    lines = [f"{tree['name']}/", "│"]
    lines.extend(create_tree(tree, ""))

    return "\n".join(lines)
    
