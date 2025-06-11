#!/usr/bin/env python3

from pydantic import BaseModel

# --------------------------------------------------------------------------------
# Pydantic Models for Type Safety
# --------------------------------------------------------------------------------

class FileToCreate(BaseModel):
    """Model for representing a file to be created."""
    path: str
    content: str

class FileToEdit(BaseModel):
    """Model for representing a file edit operation."""
    path: str
    original_snippet: str
    new_snippet: str