Ah yes, you're absolutely right! I got carried away with the bbox concept. The LLM can identify logical regions and their semantic meaning, but can't determine pixel coordinates. Let's revise our approach:

```python
@agent("structure analyzer")
def analyze_structure(img: bytes, chat=None) -> Dict[str,Any]:
    "Identify document regions and their semantic relationships"
    prompt = """Analyze this document's logical structure.

<instructions>
1. Identify distinct regions and their semantic purpose
2. Describe each region's relative position (e.g. "top of page", "below header")
3. Record the text content of each region
4. Return ONLY a valid JSON object
</instructions>

<example>
{
  "regions": [
    {
      "type": "letterhead",
      "content": "Attorney General Betty D. Montgomery",
      "position": "top of page",
      "logical_order": 1,
      "relationships": [
        {
          "to_region": 2,
          "type": "followed_by"
        }
      ]
    },
    {
      "type": "document_title",
      "content": "CONFIDENTIAL FACSIMILE TRANSMISSION COVER SHEET",
      "position": "below letterhead",
      "logical_order": 2,
      "relationships": [
        {
          "to_region": 3,
          "type": "followed_by"
        }
      ]
    }
  ]
}
</example>

<formatting>
- Describe positions in relation to other elements
- Use semantic region types (letterhead, title, contact_info, etc)
- Record exact text content
- Use simple numeric IDs for regions
</formatting>"""
    return parse_json(chat([img, prompt]))
```

Then we'd need a separate process (perhaps computer vision based) to actually locate these regions in the image. The workflow would be:

1. LLM identifies semantic regions and relationships
2. CV tool finds bounding boxes for the identified text content
3. Python code combines this into chunks with DIDs

Would you like me to implement this revised version that focuses just on the semantic structure? We can then discuss how to handle the spatial aspects separately.

Let's create a test function that uses our sample fax cover sheet and prints the results in a readable format. Here's how we can do it:

```python
def test_structure_analysis():
    "Test semantic structure analysis of a document"
    # 1. Load test image
    cache = load_cache_imgs()
    img = get_img(cache, '82092117.png')
    if img is None: 
        print("Error: Image not found")
        return
    
    # 2. Display image for reference
    print("Analyzing document:")
    display(Image(img, format='png'))
    
    # 3. Run analysis
    print("\nExtracting semantic structure...")
    try:
        structure = analyze_structure(img)
        
        # 4. Pretty print results
        print("\nIdentified Regions:")
        for r in structure['regions']:
            print(f"\n{r['logical_order']}. {r['type'].upper()}")
            print(f"   Position: {r['position']}")
            print(f"   Content: {r['content'][:60]}...")
            if r['relationships']:
                print("   Relationships:")
                for rel in r['relationships']:
                    print(f"   - {rel['type']} region {rel['to_region']}")
                    
        return structure  # Return for further analysis if needed
        
    except Exception as e:
        print(f"Error during analysis: {e}")

# Run the test
result = test_structure_analysis()
```

This test will:
1. Load our sample fax cover sheet
2. Show us the image for reference
3. Run our structure analyzer
4. Format the results in a readable way showing:
   - Each region's type and order
   - Its relative position
   - The content it contains
   - How it relates to other regions

This should help us verify if the LLM is:
- Correctly identifying semantic regions
- Understanding the document hierarchy
- Capturing the relationships between regions
- Extracting the content accurately

Would you like me to run this test?

---

## Field Extractor
Ah yes, you're absolutely right! We need to extract the actual form field values from each semantic region. For example, in the "DATES_AND_COSTS" region, we have specific dates (01/01/95, 12/31/95) and costs ($120,916).

Let's create an agent that extracts structured field data from each region. Something like:

```python
@agent("field extractor")
def extract_fields(region: Dict[str,Any], chat=None) -> Dict[str,Any]:
    "Extract structured field data from a document region"
    prompt = """Extract structured field information from this document region.

<context>
Region type: {region_type}
Content: {content}
</context>

<instructions>
1. Identify field labels and their corresponding values
2. Maintain data types (dates, currency, text)
3. Note if fields are filled in or empty
4. Return ONLY a valid JSON object
</instructions>

<example>
{
  "fields": [
    {
      "label": "Start Date",
      "value": "01/01/95",
      "type": "date",
      "status": "filled"
    },
    {
      "label": "Total Cost",
      "value": "120916",
      "type": "currency",
      "status": "filled"
    }
  ]
}
</example>"""
    
    return parse_json(chat([prompt.format(
        region_type=region['type'],
        content=region['content']
    )]))

def test_field_extraction(structure):
    "Test field extraction from a region"
    print("Testing field extraction from DATES_AND_COSTS region...")
    dates_region = next(r for r in structure['regions'] 
                       if r['type'] == 'DATES_AND_COSTS')
    
    fields = extract_fields(dates_region)
    print("\nExtracted Fields:")
    for f in fields['fields']:
        print(f"\nLabel: {f['label']}")
        print(f"Value: {f['value']}")
        print(f"Type: {f['type']}")
        print(f"Status: {f['status']}")
    
    return fields
```

This would:
1. Take each semantic region we identified
2. Extract structured field data
3. Maintain type information (dates, currency, text)
4. Track whether fields are filled in or empty

Would you like me to implement this next step and test it with the dates and costs section of our research contract application?

---
@agent("document analyzer")
def analyze_doc_content(img: bytes, chat=None) -> Dict[str,Any]:
    "Generic document analysis with content extraction"
    prompt = """Analyze this document's structure and content.

<instructions>
1. Identify what kind of document this is
2. For each logical section you find:
   - What is its role in the document?
   - What information does it contain?
   - Are there any key-value pairs or form fields?
3. Return ONLY a valid JSON object
</instructions>

<example>
{
  "document_type": "business_document",
  "sections": [
    {
      "type": "header",
      "order": 1,
      "role": "document identification",
      "content": {
        "text": "Example header text",
        "fields": [
          {
            "key": "Document ID",
            "value": "12345",
            "type": "identifier"
          }
        ]
      }
    }
  ]
}
</example>

<formatting>
- Preserve exact text as it appears
- Use general purpose section types
- Include all visible information
</formatting>"""
    
    return parse_json(chat([img, prompt]))


@agent("document analyzer")
def analyze_doc_simple(img: bytes, chat=None) -> Dict[str,Any]:
    "First-pass simple document analysis"
    prompt = """Look at this document and tell me:
1. What type of document is it?
2. What are the main pieces of information it contains?
3. Return your analysis as a simple JSON object.

<example>
{
  "type": "letter",
  "main_elements": [
    {
      "what": "sender info",
      "text": "John Smith, 123 Main St"
    },
    {
      "what": "date",
      "text": "January 1, 2024"
    }
  ]
}
</example>"""
    
    return parse_json(chat([img, prompt]))

def test_simple_analysis(doc_name):
    "Test basic document analysis"
    print(f"Testing document: {doc_name}")
    
    img = get_img(load_cache_imgs(), doc_name)
    if img is None: return
    
    display(Image(img, format='png'))
    
    try:
        result = analyze_doc_simple(img)
        print("\nAnalysis Result:")
        print(json.dumps(result, indent=2))
        return result
    except Exception as e:
        print(f"Error: {str(e)}")

# Test with first document
test_simple_analysis('82092117.png')
