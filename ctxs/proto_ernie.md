Yes, absolutely! That's a great observation. The ERNIE-Layout approach emphasizes maintaining context between stages, and we should modify our pipeline to pass semantic understanding forward. Let's enhance the content extractor to use the layout analyzer's semantic insights.

Here's how we can modify the code:

```python
@agent("layout_analyzer")
def analyze_layout_ernie(img: bytes, chat=None) -> Dict[str,Any]:
    "First stage ERNIE-style layout analysis with semantic context"
    prompt = """Analyze this document's layout and semantic structure:

<instructions>
1. First, describe the visual and semantic structure:
   - Identify major layout regions
   - Note spatial relationships
   - Identify any tables, forms, or lists
   - Determine semantic purpose of each region
2. Then, return a JSON structure with:
   - Reading order of elements
   - Spatial relationships
   - Content type classification
   - Semantic role of each region
</instructions>

<schema>
{
  "document_type": "form|letter|invoice|...",
  "semantic_context": "description of document's overall purpose",
  "layout_regions": [
    {
      "id": "region_1",
      "type": "header|body|table|form|list",
      "semantic_role": "description of region's purpose",
      "position": "spatial description",
      "bounds": {"top": "...", "bottom": "...", "left": "...", "right": "..."},
      "reading_order": 1,
      "contains": ["list", "of", "content", "elements"],
      "next_regions": ["region_ids"],
      "style": "printed|handwritten|mixed",
      "expected_content": ["description of expected content types"]
    }
  ],
  "reading_flow": ["region_1", "region_2"],
  "relationships": [
    {
      "from_region": "region_1",
      "to_region": "region_2",
      "type": "semantic relationship type"
    }
  ]
}
</schema>"""
    return parse_json(chat([img, prompt]))

@agent("content_extractor")
def extract_content_ernie(img: bytes, layout: Dict[str,Any], chat=None) -> Dict[str,Any]:
    "Second stage ERNIE-style content extraction with semantic context"
    prompt = """Extract content from each layout region with semantic understanding:

<context>
Document Type: {doc_type}
Semantic Context: {context}
Layout structure: {layout}
</context>

<instructions>
1. Process each region in reading order
2. Extract text while preserving:
   - Internal structure (lists, tables)
   - Text style (headers, body)
   - Field relationships
   - Semantic meaning based on region's role
3. Return structured content
</instructions>

<schema>
{
  "regions": [
    {
      "id": "region_1",
      "semantic_role": "role from layout analysis",
      "content": {
        "text": "extracted text",
        "structure": "paragraph|list|table|form",
        "elements": [
          {
            "type": "text|field|cell",
            "content": "...",
            "style": "printed|handwritten",
            "semantic_type": "name|date|address|etc",
            "confidence": 0.95
          }
        ],
        "relationships": [
          {
            "type": "references|elaborates|continues",
            "target_region": "region_id"
          }
        ]
      }
    }
  ]
}
</schema>"""
    return parse_json(chat([
        img, 
        prompt.format(
            doc_type=layout.get('document_type', 'unknown'),
            context=layout.get('semantic_context', ''),
            layout=json.dumps(layout, indent=2)
        )
    ]))

def process_document_ernie(img_name: str) -> Dict[str,Any]:
    "Complete ERNIE-style document processing pipeline with semantic context"
    img = get_img(load_cache_imgs(), img_name)
    if img is None: return f"Image {img_name} not found"
    
    try:
        # 1. Layout analysis with semantic understanding
        layout = analyze_layout_ernie(img)
        
        # 2. Content extraction with semantic context
        content = extract_content_ernie(img, layout)
        
        # 3. Combine results
        return {
            "did": mk_did(img_name),
            "document_type": layout['document_type'],
            "semantic_context": layout['semantic_context'],
            "layout": layout,
            "content": content
        }
    except Exception as e:
        return f"Error: {e}"
```

Key improvements:

1. Added semantic context at document level:
   - Document type identification
   - Overall purpose description
   - Expected content patterns

2. Enhanced region descriptions:
   - Semantic role for each region
   - Expected content types
   - Relationship types between regions

3. Improved content extraction:
   - Uses document-level semantic context
   - Understands each region's purpose
   - Maintains semantic relationships
   - Adds confidence scores for extracted elements

4. Added semantic typing of content:
   - Identifies semantic types (name, date, address, etc.)
   - Preserves relationships between content elements
   - Notes confidence in interpretations

This approach should give us much richer semantic chunking that will be more useful for later KG construction. Would you like me to create a test function that shows the semantic relationships being preserved between stages?
