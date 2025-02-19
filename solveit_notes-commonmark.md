

``` python
# Create chat and get response
imgchat = Chat(model)
response = imgchat([img, prompt])

# Parse the XML response
try:
    # The response needs to be accessed as a string first
    # Let's print the raw response to see what we're getting
    print("Raw response:")
    print(response)
    
    # Then we can try to extract the XML
    # We might need to use BeautifulSoup to find the XML content within the response
    soup = bs(str(response), 'xml')
    doc = Document(str(soup.find('document')))
    
    # Now we can access structured data
    metadata = doc.find('metadata')
    structure = doc.find('structure')
    print("\nParsed data:")
    print(f"Document type: {metadata.find('type').text if metadata else 'Not found'}")
except Exception as e:
    print(f"Error parsing response: {e}")
```

------------------------------------------------------------------------

Yes! The tools-lm package’s XML support will be perfect for this. Let’s
modify our approach to use the XML structure more effectively and make
the results easily parseable:

``` python
from toolslm.xml import *

# Define our structured prompt with XML tags that match the toolslm expectations
prompt = """<task>
Analyze this document image and extract its structure and content.
</task>

<instructions>
Act as an expert document structure analyst. Extract and structure the document information hierarchically.
</instructions>

<output_format>
<document>
    <metadata>
        <type></type>
        <title></title>
        <form_id></form_id>
        <date></date>
    </metadata>
    <structure>
        <header>
            <fields></fields>
        </header>
        <body>
            <sections></sections>
        </body>
        <footer>
            <fields></fields>
        </footer>
    </structure>
</document>
</output_format>

<thinking>
1. Identify document type and metadata
2. Analyze visual layout and sections
3. Extract form fields and relationships
4. Structure hierarchically in XML format
</thinking>

Please provide your analysis in valid XML format using the structure above."""

# Create chat and get response
imgchat = Chat(model)
response = imgchat([img, prompt])

# Parse the XML response
try:
    # Extract XML content from response (assuming it's in the response text)
    xml_content = response.content
    # Parse using toolslm's XML support
    doc = Document(xml_content)
    # Now we can access structured data
    metadata = doc.find('metadata')
    structure = doc.find('structure')
    print(f"Document type: {metadata.find('type').text}")
except Exception as e:
    print(f"Error parsing response: {e}")
```

This approach has several advantages: 1. Uses native XML support from
toolslm 2. Makes the response easily parseable 3. Maintains structure
that aligns with KAG’s knowledge representation 4. Provides clear
validation of the output format

Would you like me to run this and we can then refine based on the
results?

Ah, now I understand! We want to extract the document’s structural
semantics - like “this is a form with a header containing identifying
fields, a body with expenditure entries, and a footer with notes” -
rather than the specific data within those fields. Let’s modify our
prompt to focus on the document’s semantic structure:

``` python
prompt = """<task>
Analyze this document's form structure and semantic organization, focusing on the types of fields and their relationships rather than their contents.
</task>

<instructions>
Act as a document structure analyst. Identify:
1. The semantic organization of the form
2. Types of fields and their purposes
3. Logical groupings and hierarchies
4. Relationships between different sections
</instructions>

<output_format>
<document_schema>
    <form_type>
        <purpose></purpose>
        <primary_entities></primary_entities>
    </form_type>
    <layout_structure>
        <header>
            <field_types></field_types>
            <semantic_purpose></semantic_purpose>
        </header>
        <body>
            <section_types></section_types>
            <field_groups></field_groups>
            <repeating_structures></repeating_structures>
        </body>
        <footer>
            <field_types></field_types>
            <semantic_purpose></semantic_purpose>
        </footer>
    </layout_structure>
    <relationships>
        <field_dependencies></field_dependencies>
        <calculation_flows></calculation_flows>
        <validation_rules></validation_rules>
    </relationships>
</document_schema>
</output_format>

<thinking>
1. First, identify the form's overall purpose and structure
2. Analyze field types and their semantic roles
3. Identify repeating patterns and data structures
4. Map relationships and dependencies between sections
</thinking>

Please analyze the document's structure and provide the schema in XML format."""

# Create chat and get response
imgchat = Chat(model)
response = imgchat([img, prompt])
print(response)
```

This revised prompt should: 1. Focus on structural patterns rather than
content 2. Identify field types and their purposes 3. Map relationships
between different parts of the form 4. Create a schema that could be
applied to similar forms

Would you like me to run this updated version?
