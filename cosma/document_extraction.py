"""First phase of agentic workdflow mulimodal prompt chain to do Knowledge Extraction from Document."""

# AUTOGENERATED! DO NOT EDIT! File to edit: ../00_core.ipynb.

# %% auto 0
__all__ = ['Region', 'SpatialRel', 'DocLayout', 'RegionContent', 'parse_json']

# %% ../00_core.ipynb 3
from fastcore.all import *
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from pathlib import Path
from functools import lru_cache
import json

# %% ../00_core.ipynb 6
@dataclass
class Region:
    "A region represents a distinct area in a document with specific content and purpose"
    id: str
    name: str 
    type: str
    order: int
    position: str
    bounds: str = ''
    next_regions: List[str] = field(default_factory=list)
    contains: List[str] = field(default_factory=list)
    
    def __repr__(self): return (
        f"\n{self.name} (type: {self.type})\n"
        f"  Position: {self.position}"
        + (f"\n  Contains: {', '.join(self.contains)}" if self.contains else '')
        + (f"\n  Next: {', '.join(self.next_regions)}" if self.next_regions else '')
    )

# %% ../00_core.ipynb 7
@dataclass 
class SpatialRel:
    "Describes how regions are spatially related to each other in the document"
    from_region: str
    to_region: str  
    relationship: str
    
    def __repr__(self): return f"{self.from_region} {self.relationship} {self.to_region}"

# %% ../00_core.ipynb 8
@dataclass
class DocLayout:
    "Complete document layout structure including regions and their relationships"
    document_type: str
    regions: List[Region]
    reading_flow: List[str] = field(default_factory=list)
    spatial_relationships: List[SpatialRel] = field(default_factory=list)
    
    @classmethod
    def from_dict(cls, d:Dict) -> 'DocLayout': 
        "Create layout from parsed JSON dict output by LLM"
        layout = d['layout']
        return cls(
            document_type=d['document_type'],
            regions=[Region(
                id=r.get('id', f"r{i+1}"),
                name=r['name'],
                type=r['type'], 
                order=r.get('order', i+1),
                position=r.get('position', 'unknown'),
                bounds=r.get('bounds', ''),
                next_regions=r.get('next_regions', []),
                contains=r.get('contains', [])
            ) for i,r in enumerate(layout['regions'])],
            reading_flow=layout.get('reading_flow', []),
            spatial_relationships=[SpatialRel(**r) for r in layout.get('spatial_relationships', [])]
        )

# %% ../00_core.ipynb 9
@dataclass
class RegionContent:
    "Structured content extracted from a document region including semantic information"
    content: str
    concepts: List[Dict[str, str]]
    document_purpose: str  
    relationships: List[Dict[str, str]]
    
    def __repr__(self): return (
        f"Content:\n{self.content}\n\n"
        + f"Concepts:\n" + "\n".join(f"- {c['type']}: {c['value']}" for c in self.concepts)
        + f"\n\nPurpose: {self.document_purpose}\n\n"
        + f"Relationships:\n" + "\n".join(
            f"- {r['type']} → {r['target']}: {r['description']}" 
            for r in self.relationships)
    )

# %% ../00_core.ipynb 14
def parse_json(s: str) -> dict:
    "Parse JSON from raw LLM response, handling markdown code blocks"
    if isinstance(s, (dict,list)): return s
    if hasattr(s, 'choices'): s = s.choices[0].message.content
    if '```' in s:
        blocks = s.split('```')
        for i,block in enumerate(blocks):
            if block.strip().lower() == 'json' and i+1 < len(blocks): s = blocks[i+1]
    s = s.strip()
    if not s.startswith('{'): s = s[s.find('{'):]
    if not s.endswith('}'): s = s[:s.rfind('}')+1]
    return json.loads(s)
