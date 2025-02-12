# The knowledge representation model for KAG

Based on the documents, KAG uses a knowledge representation model called LLMFriSPG that extends the SPG (Semantic Property Graph) framework to be more friendly to large language models. Let me explain the key aspects of this representation model:

The basic structure is defined as ℳ = {𝒯, ρ, 𝒞, ℒ}, where:

1. Type System (𝒯):
- EntityTypes and EventTypes that follow object-oriented principles (e.g., Person, Organization)
- Pre-defined properties and relations compatible with LPG (Labeled Property Graph) syntax

2. Properties Framework:
For any type t, properties are organized into three categories:
- ptc: Pre-defined properties by domain experts (static/knowledge area)
- ptf: Properties added in an ad-hoc manner (dynamic/information area) 
- ptb: System built-in properties, which include these fixed properties:

The key built-in properties (ptb) are:

- supporting_chunks: Links to the original text chunks containing the instance
- description: General descriptive information specific to the class or instance
- summary: Summary of the instance or relation in the original document context  
- belongTo: Represents inductive semantics from instance to concept

3. Document Structure:
- Defines a special EntityType called "Chunk" for document segments
- Chunk properties include:
  - id: Composite field of articleID#paraCode#idInPara
  - summary: Summary of the chunk content
  - mainText: The actual content

4. Concept System (𝒞):
- ConceptTypes for managing taxonomies and concept hierarchies
- Text-based concept trees where each concept node has a unique ConceptType
- Supports semantic alignment between instances and concepts

This representation model aims to:
- Support both schema-free information extraction and schema-constrained expert knowledge
- Enable mutual indexing between graph structures and text chunks
- Maintain traceability to original document context
- Allow for dynamic property addition while preserving structured knowledge
- Bridge between unstructured text and formal knowledge representation

The design specifically accommodates LLMs by providing rich textual context (through description and summary properties) and maintaining connections to source documents (through supporting_chunks). This helps LLMs better understand and reason about the knowledge while maintaining formal structure for traditional knowledge graph operations.

This representation is particularly powerful because it allows KAG to operate across different levels of knowledge formalization - from unstructured text through semi-structured information to fully formalized knowledge - while maintaining semantic connections between these levels. This is essential for professional domain applications that need both the flexibility of text processing and the rigor of formal knowledge representation.

## Properties defined by KAG
Based on the documents, I can identify the following properties that are defined in the KAG/LLMFriSPG model:

Core Built-in Properties (ptb):
1. supporting_chunks: Links that connect instances to their source text chunks in the original documents. This enables traceability between the knowledge graph and source materials.

2. description: Contains general descriptive information that can be attached at two levels:
   - When attached to a type (tk): Provides global description for that type
   - When attached to an instance (ei): Provides instance-specific descriptive information consistent with the original document context

3. summary: A condensed representation of either:
   - An instance (ei)
   - A relation (rj)

4. belongTo: Represents the inductive relationship that connects instances to their concepts in the concept hierarchy

Chunk Entity Properties:
1. id: A composite identifier made up of:
   - articleID: The globally unique article identifier
   - paraCode: The paragraph code within the article
   - idInPara: The sequential code of the chunk within the paragraph
   These are concatenated with "#" as the connector

2. mainText: The actual content of the chunk

3. summary: A summary of the chunk's content

The model also supports two categories of additional properties:

- ptc (Static/Knowledge Area):
  - Pre-defined properties by domain experts
  - Subject to schema constraints
  - Used primarily for professional decision-making applications

- ptf (Dynamic/Information Area):
  - Properties added in an ad-hoc manner
  - More flexible and schema-free
  - Used primarily for information retrieval applications

Both ptc and ptf share the same conceptual terminology and can coexist in the instance storage space, allowing applications to balance between rigorous knowledge representation and flexible information handling based on their specific needs.

This property structure enables KAG to maintain clear connections between formal knowledge structures and original document contexts while supporting both strict domain knowledge and flexible information extraction.
