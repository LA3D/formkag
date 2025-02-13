Based on our progress and "Da Plan", let's implement the next critical pieces in a structured way. I suggest we start with enhancing our document processing layer and knowledge representation first:

1. Let's create an enhanced analyzer that implements the EntityTypes and ConceptTypes:

```python
@tool
def identify_entities(content: dict) -> dict:
    "Extract entities and their types from document content"
    chat = Chat(model)
    prompt = """Given this document content, identify all entities and their types.
    Return ONLY a JSON object with format: {"entities": [{"id": "", "type": "", "value": "", "confidence": 0.0}]}"""
    return parse_json(chat([json.dumps(content), prompt]))

@agent("semantic analyzer")
def analyze_doc_semantic(img: bytes, chat=None) -> dict:
    "Enhanced document analysis with semantic structure"
    base = analyze_doc(img)  # Get basic structure
    
    # Define our enhanced schema
    schema = {
        "document": {
            "type": base.get('type'),
            "metadata": base.get('metadata', {}),
        },
        "entities": [],  # Will be filled by identify_entities
        "relationships": [],  # Will store entity relationships
        "concepts": {
            "document_class": "",
            "confidentiality_level": "",
            "business_context": ""
        }
    }
    
    # Extract entities from content
    entities = identify_entities(base)
    schema["entities"] = entities.get("entities", [])
    
    return schema
```

2. Let's create a function to convert our semantic analysis to RDF:

```python
def create_rdf_graph(doc_analysis: dict) -> Graph:
    "Convert document analysis to RDF graph following KAG model"
    g = Graph()
    
    # Bind our namespaces
    g.bind('kag', Namespace('http://example.com/kag#'))
    g.bind('ex', Namespace('http://example.com/ex#'))
    g.bind('exDynamic', Namespace('http://example.com/dynamic#'))
    
    KAG = Namespace('http://example.com/kag#')
    EX = Namespace('http://example.com/ex#')
    DYNAMIC = Namespace('http://example.com/dynamic#')
    
    # Create document node
    doc_uri = EX[f"doc_{hash(str(doc_analysis))[:8]}"]
    g.add((doc_uri, RDF.type, KAG.Document))
    
    # Add metadata
    for k,v in doc_analysis['document']['metadata'].items():
        g.add((doc_uri, DYNAMIC[k], Literal(v)))
    
    # Add entities
    for entity in doc_analysis['entities']:
        entity_uri = EX[f"entity_{entity['id']}"]
        g.add((entity_uri, RDF.type, KAG[entity['type']]))
        g.add((entity_uri, KAG.value, Literal(entity['value'])))
        g.add((doc_uri, KAG.hasEntity, entity_uri))
    
    return g
```

Let's test this enhanced workflow:

```python
def test_semantic_doc(img_name='82092117.png'):
    "Test semantic document analysis with RDF conversion"
    img = get_img(load_cache_imgs(), img_name)
    if img is None: return f"Image {img_name} not found"
    try:
        # Get semantic analysis
        analysis = analyze_doc_semantic(img)
        # Convert to RDF
        graph = create_rdf_graph(analysis)
        # Return both for inspection
        return {'analysis': analysis, 'graph': graph.serialize(format='turtle')}
    except Exception as e: 
        return f"Error: {e}"
```

Would you like me to run this test so we can see how it performs with our example document? Based on the results, we can then:

1. Refine the entity extraction
2. Add the relationship detection
3. Implement the concept hierarchy
4. Add the validation rules

Let me know if you want to proceed with testing or if you'd like to modify the approach first!


## Document Chunker protype
@agent("document chunker")
def chunk_document(img: bytes, chat=None) -> Dict[str,Any]:
    "Create document chunks with unique DIDs and spatial relationships"
    schema = {
        "chunks": [{
            "did": "did:doc:...",  # DID for the chunk
            "bbox": {"x":0, "y":0, "w":0, "h":0},  # Spatial location
            "content": "",  # Raw text content
            "type": "",    # Section type
            "relationships": [{  # Spatial/logical relationships
                "to_chunk": "did:doc:...",
                "type": "contains|follows|references"
            }]
        }],
        "document_did": "did:doc:..."  # Root document DID
    }
    prompt = f"Analyze this document and return ONLY a JSON object matching:\n{json.dumps(schema, indent=2)}"
    return parse_json(chat([img, prompt]))

@agent("knowledge extractor") 
def extract_knowledge(chunks: Dict[str,Any], chat=None) -> Dict[str,Any]:
    "Extract structured knowledge while maintaining chunk references"
    schema = {
        "entities": [{
            "did": "did:doc:...",  # Entity DID
            "type": "",  # Entity type
            "value": "", # Extracted value
            "source_chunks": ["did:doc:..."],  # DIDs of source chunks
            "confidence": 0.0
        }],
        "relationships": [{
            "did": "did:doc:...",
            "type": "",
            "from_entity": "did:doc:...",
            "to_entity": "did:doc:...", 
            "source_chunks": ["did:doc:..."]
        }]
    }
    return parse_json(chat([json.dumps(chunks), prompt]))

