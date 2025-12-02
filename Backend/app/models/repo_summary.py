from pydantic import BaseModel, HttpUrl 
from typing import List, Optional


# What the User provides when requesting a README to be generated
class ReadmeRequest(BaseModel):
    repo_url : HttpUrl
    include_badges : bool = True
    include_installation: bool = True
    extra_notes : Optional[str] = None


# The information needed to be satisfied for generation (intermediate holder)
class ReadmeInfo(BaseModel):
    repo_url : HttpUrl
    repo_owner: str
    repo_name : str
    repo_summary : str
    repo_features : str = "Not extracted yet."
    repo_languages: str = "Not extracted yet."
    repo_techstack : str = "Not extracted yet."
    repo_structure : str = "Not extracted yet."
    repo_pipeline : str = "Not extracted yet."
    repo_localrun: str = "Not extracted yet."

class ReadmeResponse(BaseModel):
    content: str # Returns the README.md

class FinalizeReadmeRequest(BaseModel):
    content: str
    repo_Url: HttpUrl

class FinalizeReadmeResponse(BaseModel):
    message: str




