# EmployeeAssist AI

EmployeeAssist AI is an intelligent HR support application built as an AI engineering portfolio project.

## Overview

The application helps employees:

- Ask questions about approved HR policies
- Retrieve relevant policy information using semantic search
- Submit annual leave requests
- Receive safe fallback responses when information is unavailable

## Architecture

Employee
   |
   v
Streamlit Web Application
   |
   +-- HR Policy Question
   |       |
   |       v
   |   Sentence Transformer Embeddings
   |       |
   |       v
   |   Cosine Similarity Search
   |       |
   |       v
   |   Approved HR Knowledge Base
   |
   +-- Annual Leave Request
           |
           v
       Input Validation
           |
           v
       Leave Request Action
           |
           v
       CSV Data Store

## Technologies

- Python
- Streamlit
- Sentence Transformers
- Scikit-learn
- Semantic Search
- Vector Embeddings
- CSV persistence
- Microsoft Copilot Studio prototype

## AI / Agent Capabilities

### Knowledge Retrieval
HR policy content is converted into vector embeddings using the
`all-MiniLM-L6-v2` sentence-transformer model.

Employee questions are embedded and compared with policy content using
cosine similarity.

### Grounded Responses
The application returns information retrieved from the approved HR
knowledge base rather than inventing company policies.

### Guardrail / Fallback
When sufficiently relevant information cannot be found, the application
directs the employee to HR rather than generating an unsupported policy.

### Business Action
Employees can submit an annual leave request. The application validates
the request and persists it with a Pending Manager Approval status.

## Example Questions

- How many days of annual leave do full-time employees receive?
- I've been sick for 8 days. What do I need to do?
- Can I work remotely three days per week?
- Can I bring my dog to the office?

## Disclaimer

This project uses fictional Contoso Services HR policies and demonstration
data. It is intended solely as an AI engineering portfolio project.