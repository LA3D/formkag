ADW Blog: https://www.llamaindex.ai/blog/introducing-agentic-document-workflows

Announcing our Document Research Assistant, a collaboration with NVIDIA!

  * Enterprise
  * LlamaParse
  * Framework
  * Community
  * Careers
  * Blog

© 2024 LlamaIndex

LlamaIndex • 2025-01-09

# Introducing Agentic Document Workflows

  * Generative AI Use Cases
  * Agentic Document Workflows

We’re kicking off 2025 by introducing a new architecture for applying agents on top of your documents: Agentic Document Workflows (ADW). This architecture combines document processing, retrieval, structured outputs, and agentic orchestration to enable end-to-end knowledge work automation. It is a step beyond both traditional Intelligent Document Processing (IDP) and RAG paradigms, which are focused on small, isolated steps of extraction and question-answering respectively, and helps to fulfill the promise of agents in dramatically increasing knowledge productivity.

## Moving Beyond Basic RAG

While RAG has emerged as a powerful pattern for grounding LLMs in enterprise data, many real-world document workflows require more sophisticated orchestration. Consider a typical contract review workflow: an analyst needs to extract key clauses, cross-reference regulatory requirements, identify potential risks, and generate compliance recommendations. This requires not just information retrieval, but structured reasoning and decision support.

Traditional approaches often struggle with complex workflows that go beyond simple extraction or matching. In real organizations:

  * Documents don't exist in isolation - processes involve contracts, policies, emails, and forms working together
  * Decisions span multiple steps - from data extraction to validation to approval to recommendations
  * Context and state must be maintained across the entire process
  * Multiple systems need to coordinate - parsers, retrievers, and business logic engines

Agentic Document Workflows (ADW) address these challenges by treating documents as part of broader business processes. An ADW system can maintain state across steps, apply business rules, coordinate different components, and take actions based on document content - not just analyze it.

## Building Intelligent Document Agents

We've developed a set of reference architectures that demonstrate how to combine LlamaCloud's enterprise-grade parsing and retrieval capabilities with intelligent agents. Each architecture shows how to build systems that can understand context, maintain state, and drive multi-step processes.

The core of each workflow is a document agent that orchestrates the entire process. These agents:

  * Extract and structure information from input documents using LlamaParse
  * Maintain state about the document context and process stage
  * Retrieve and analyze relevant reference materials from a knowledge base (LlamaCloud)
  * Generate actionable recommendations based on business rules

By maintaining state throughout the process, agents can handle complex multi-step workflows that go beyond simple extraction or matching. This approach allows them to build deep context about the documents they're processing while coordinating between different system components.

Let's explore this through some real-world sample use cases. These + other use cases are also directly available as notebook resources.

## Contract Review: Intelligent Compliance Analysis

The contract review workflow showcases how document agents can perform sophisticated analysis across multiple documents. When analyzing a vendor agreement, the agent parses complex contract structures, identifies key clauses, and matches them against a knowledge base of regulatory requirements stored in LlamaCloud.

This allows it to surface potential compliance issues and provide structured recommendations about areas that require human review - such as non-standard terms, missing provisions, or clauses that may conflict with regulations. The system serves as an intelligent assistant, helping legal teams work more efficiently while keeping humans firmly in control of final decisions.

## Patient Case Summaries: Contextual Understanding

The exploding volume of healthcare documentation presents unique challenges that demonstrate the power of intelligent document processing to accelerate the work of physicians. Our patient case summary agent doesn't just extract information from medical records, it can group related conditions, treatments and outcomes together, aiding diagnosis and treatment.

The workflow can parse complex medical documents, including lab results and clinical notes, while maintaining the critical context of a patient's history. By matching this information against medical guidelines stored in LlamaCloud, the agent can generate comprehensive case summaries that highlight key clinical insights for physician review.

## Invoice Processing: Optimizing Business Operations

Our invoice processing workflow shows how intelligent agents can add business intelligence to routine tasks. The agent goes beyond basic data extraction to support optimization of payment timing based on vendor agreements and early payment discounts.

Using LlamaParse to accurately extract line items and payment terms, combined with LlamaCloud's retrieval capabilities, the agent can verify pricing against contracted rates and suggest optimal payment strategies. This transforms a simple document processing task into a tool for working capital optimization.

## Auto Insurance Claims Processing: Structured Analysis Support

Our auto insurance claims workflow demonstrates how intelligent document processing can support—not replace—human decision-making in complex processes. The agent helps claims processors by organizing and structuring information from multiple documents: parsing incoming claims forms, matching relevant sections of policy documents, and presenting key details in a clear format.

Importantly, the system is designed to augment human expertise, not make final decisions. It helps claims processors by surfacing relevant policy details and organizing information, while leaving all coverage and settlement decisions firmly in human hands. This showcases how AI can streamline processes while maintaining appropriate human oversight in sensitive domains.

## Building Production-Ready Solutions

Each of these examples is implemented as a detailed Jupyter notebook that you can run and adapt. The workflows demonstrate our approach to production-grade document processing: combining LlamaParse's advanced document understanding capabilities with LlamaCloud's robust retrieval and our agentic framework.

The notebooks show how to handle real-world complexities like error handling, validation, and scalability. They're designed to serve as starting points for your own implementations, with clear examples of how to customize the logic for your specific use cases.

## Getting Started

We're seeing enterprises across industries adopt these more advanced patterns beyond basic chatbots. Ready to start building? You can:

  * Explore our example implementations 
    * Contract Review Workflow
    * Patient Case Summary Workflow
    * Invoice Processing Workflow
    * Invoice Unit Standardization Workflow
    * Invoice + SKU Matching Workflow
    * Auto Insurance Claims Workflow
  * Sign up for LlamaCloud to access enterprise-grade parsing and retrieval
  * If you’re interested in building this in an enterprise setting, come talk to us.
  * Join our Discord community to discuss your use cases and get implementation support

Over the coming weeks, we’ll be announcing a _lotd_ of new feature releases and educational deep-dives that will allow you to build production agentic document workflows for an increasing number of use cases. Stay tuned!

## Related articles

  * Introducing AgentWorkflow: A Powerful System for Building AI Agent Systems

2025-01-22

  * Case Study: Netchex: More Efficient HR Operations with LlamaIndex Powered AskHR + Netchex AI

2024-09-04

  * Bridging the Gap in Crisis Counseling: Introducing Counselor Copilot

