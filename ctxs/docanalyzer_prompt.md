```python
@agent("document analyzer")
def analyze_doc_content(img: bytes, chat=None) -> Dict[str,Any]:
    "Single-pass document analysis with form field extraction"
    prompt = """Analyze this document and extract both its structure and content.

<instructions>
1. First identify the document type and overall purpose
2. For each major section:
   - Describe its purpose
   - List any form fields found
   - Extract actual values if present
3. Return ONLY a valid JSON object
</instructions>

<example>
{
  "document_type": "research_contract_application",
  "purpose": "Application for research funding",
  "sections": [
    {
      "type": "project_details",
      "order": 1,
      "purpose": "Basic project information",
      "fields": [
        {
          "label": "Project Title",
          "value": "Mechanisms of Chronic Ozone Exposure",
          "type": "text"
        },
        {
          "label": "Start Date",
          "value": "01/01/95",
          "type": "date"
        }
      ]
    }
  ]
}
</example>

<formatting>
- Keep field values exactly as they appear
- Include all visible text in appropriate sections
- Maintain hierarchical structure
</formatting>"""
    
    return parse_json(chat([img, prompt]))
```
