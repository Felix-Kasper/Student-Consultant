# AI Study Consultant

An AI-powered document intelligence API that transforms
academic PDF documents into personalized learning insights.

The project combines document processing, structured LLM
outputs, personalization and automated study planning.

## Overview

AI Study Consultant allows students to upload academic
documents such as:

- lecture notes
- scientific papers
- case studies
- university scripts
- study materials

The system analyzes the document and generates:

- Document summary
- Key concepts
- Exam-relevant topics
- Potential exam questions
- Answers
- Flashcards
- Difficult concepts explained simply
- Personalized recommendations
- A suggested study strategy

## Architecture

                  PDF
                   |
                   v
           +---------------+
           | PDF Extraction|
           +-------+-------+
                   |
                   v
           +---------------+
           | Document      |
           | Preparation   |
           +-------+-------+
                   |
                   v
           +---------------+
           | OpenAI        |
           | Responses API |
           +-------+-------+
                   |
                   v
           +---------------+
           | Structured    |
           | JSON Output   |
           +-------+-------+
                   |
                   v
           +---------------+
           | Personalized  |
           | Study Analysis|
           +---------------+
