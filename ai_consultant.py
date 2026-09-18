import io
import json
import os

from pypdf import PdfReader
from openai import OpenAI


# ---------------------------------------------------------
# OpenAI Client
# ---------------------------------------------------------

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-5.6-luna"
)


# ---------------------------------------------------------
# PDF TEXT EXTRACTION
# ---------------------------------------------------------

def extract_pdf_text(pdf_bytes: bytes) -> str:

    pdf_stream = io.BytesIO(pdf_bytes)

    reader = PdfReader(pdf_stream)

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text()

        if text:
            pages.append(
                f"\n--- PAGE {page_number} ---\n{text}"
            )

    document_text = "\n".join(pages)

    if not document_text.strip():
        raise ValueError(
            "No readable text could be extracted from the PDF."
        )

    return document_text


# ---------------------------------------------------------
# TEXT LIMIT
# ---------------------------------------------------------

def prepare_document(text: str) -> str:

    # Prevent accidentally sending enormous documents.
    max_characters = 100_000

    if len(text) <= max_characters:
        return text

    return (
        text[:max_characters]
        + "\n\n[DOCUMENT TRUNCATED FOR ANALYSIS]"
    )


# ---------------------------------------------------------
# STUDY ANALYSIS
# ---------------------------------------------------------

def analyze_document(
    pdf_bytes: bytes,
    filename: str,
    profile: dict
) -> dict:

    document_text = extract_pdf_text(pdf_bytes)

    document_text = prepare_document(
        document_text
    )

    profile_text = json.dumps(
        profile,
        ensure_ascii=False,
        indent=2
    )

    instructions = """
You are an advanced AI Study Consultant.

Your task is to analyze academic documents for a university
student.

IMPORTANT RULES:

1. Base your analysis primarily on the supplied document.
2. Do not invent facts that are not supported by the document.
3. Clearly distinguish document content from your own explanation.
4. Adapt the analysis to the student's profile.
5. Focus on learning efficiency and exam preparation.
6. Do not unnecessarily summarize every paragraph.
7. Identify the concepts that actually matter.
8. Explain difficult concepts in simple language.
9. Generate realistic exam questions based on the document.
10. If the document does not contain enough information for a
    specific conclusion, explicitly say so.

The output must be useful to a real university student.
"""


    user_prompt = f"""
STUDENT PROFILE
================

{profile_text}


DOCUMENT
================

Filename:
{filename}

Content:

{document_text}


ANALYZE THIS DOCUMENT.
"""


    response = client.responses.create(
        model=MODEL,

        instructions=instructions,

        input=user_prompt,

        text={
            "format": {
                "type": "json_schema",
                "name": "study_analysis",
                "strict": True,
                "schema": {
                    "type": "object",

                    "properties": {

                        "document": {
                            "type": "object",
                            "properties": {

                                "title": {
                                    "type": "string"
                                },

                                "document_type": {
                                    "type": "string"
                                },

                                "estimated_difficulty": {
                                    "type": "string"
                                },

                                "overall_summary": {
                                    "type": "string"
                                }

                            },

                            "required": [
                                "title",
                                "document_type",
                                "estimated_difficulty",
                                "overall_summary"
                            ],

                            "additionalProperties": False
                        },


                        "key_concepts": {
                            "type": "array",

                            "items": {
                                "type": "object",

                                "properties": {

                                    "concept": {
                                        "type": "string"
                                    },

                                    "definition": {
                                        "type": "string"
                                    },

                                    "why_it_matters": {
                                        "type": "string"
                                    },

                                    "importance": {
                                        "type": "integer"
                                    }

                                },

                                "required": [
                                    "concept",
                                    "definition",
                                    "why_it_matters",
                                    "importance"
                                ],

                                "additionalProperties": False
                            }
                        },


                        "exam_topics": {
                            "type": "array",

                            "items": {
                                "type": "object",

                                "properties": {

                                    "topic": {
                                        "type": "string"
                                    },

                                    "reason": {
                                        "type": "string"
                                    },

                                    "priority": {
                                        "type": "integer"
                                    }

                                },

                                "required": [
                                    "topic",
                                    "reason",
                                    "priority"
                                ],

                                "additionalProperties": False
                            }
                        },


                        "exam_questions": {
                            "type": "array",

                            "items": {
                                "type": "object",

                                "properties": {

                                    "question": {
                                        "type": "string"
                                    },

                                    "answer": {
                                        "type": "string"
                                    },

                                    "difficulty": {
                                        "type": "string"
                                    }

                                },

                                "required": [
                                    "question",
                                    "answer",
                                    "difficulty"
                                ],

                                "additionalProperties": False
                            }
                        },


                        "flashcards": {
                            "type": "array",

                            "items": {
                                "type": "object",

                                "properties": {

                                    "front": {
                                        "type": "string"
                                    },

                                    "back": {
                                        "type": "string"
                                    }

                                },

                                "required": [
                                    "front",
                                    "back"
                                ],

                                "additionalProperties": False
                            }
                        },


                        "difficult_concepts": {
                            "type": "array",

                            "items": {
                                "type": "object",

                                "properties": {

                                    "concept": {
                                        "type": "string"
                                    },

                                    "simple_explanation": {
                                        "type": "string"
                                    },

                                    "example": {
                                        "type": "string"
                                    }

                                },

                                "required": [
                                    "concept",
                                    "simple_explanation",
                                    "example"
                                ],

                                "additionalProperties": False
                            }
                        },


                        "personalized_recommendations": {
                            "type": "array",

                            "items": {
                                "type": "string"
                            }
                        },


                        "study_plan": {
                            "type": "object",

                            "properties": {

                                "recommended_order": {
                                    "type": "array",
                                    "items": {
                                        "type": "string"
                                    }
                                },

                                "estimated_minutes": {
                                    "type": "integer"
                                },

                                "strategy": {
                                    "type": "string"
                                }

                            },

                            "required": [
                                "recommended_order",
                                "estimated_minutes",
                                "strategy"
                            ],

                            "additionalProperties": False
                        }

                    },

                    "required": [
                        "document",
                        "key_concepts",
                        "exam_topics",
                        "exam_questions",
                        "flashcards",
                        "difficult_concepts",
                        "personalized_recommendations",
                        "study_plan"
                    ],

                    "additionalProperties": False
                }
            }
        }
    )


    # Convert structured model output into Python object
    result = json.loads(
        response.output_text
    )

    # Add technical metadata
    result["_metadata"] = {
        "filename": filename,
        "model": MODEL,
        "characters_analyzed": len(document_text)
    }

    return result
