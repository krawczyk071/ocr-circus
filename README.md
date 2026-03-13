
## Application Overview

__OCR-Circus__ is a sophisticated PDF-to-Markdown conversion application that uses Large Language Models (LLMs) with vision capabilities to perform Optical Character Recognition (OCR) on scanned documents and convert them into clean, structured markdown files.


## detials
documentation/OCR_Circus_Application_Documentation.md

## Key Features

1. __Multi-LLM Support__: Supports OpenAI's GPT-4o-mini, GPT-4o, and Google's Gemini 2.0 Flash
2. __PDF Processing__: Extracts pages from PDFs and converts them to high-resolution screenshots
3. __OCR Processing__: Uses LLMs to perform OCR on each page image
4. __Markdown Generation__: Converts OCR output into clean, structured markdown
5. __Batch Processing__: Handles multi-page documents efficiently
6. __Cost Calculation__: Includes tools to estimate processing costs
7. __Web Interface__: Provides both Streamlit web app and direct Python API

## Architecture Components

The application is organized into several key modules:

### Core Application (`app/`)

- __`app.py`__: Main application logic and orchestration
- __`functions_llm.py`__: LLM integration and prompt management
- __`functions_pdf.py`__: PDF processing and image extraction
- __`functions.py`__: Utility functions for file operations
- __`streamlit_app.py`__: Web interface using Streamlit
- __`web_app.py`__: Alternative web interface implementation

### Jupyter Notebooks (Development/Testing)

- __`cost_calc.ipynb`__: Cost calculation and token counting utilities
- __`demo.ipynb`__: Basic demonstration of LLM vision capabilities
- __`direct_openai.ipynb`__: Direct OpenAI API usage examples
- __`pdf_handling.ipynb`__: PDF processing techniques and utilities
- __`wc1.ipynb`__: Working example with vision model integration

## Processing Workflow

1. __PDF Input__: Accept PDF files (local or uploaded)
2. __Page Selection__: Optionally select specific page ranges
3. __Image Extraction__: Convert each page to high-resolution PNG images
4. __LLM Processing__: Send each image to the selected LLM with OCR prompt
5. __Markdown Generation__: Convert LLM responses to markdown format
6. __File Organization__: Save individual page markdown files
7. __Document Assembly__: Merge all pages into a single markdown document

## Key Technologies

- __PyMuPDF (fitz)__: PDF processing and image extraction
- __LangChain__: LLM integration and prompt management
- __OpenAI API__: GPT-4o vision models
- __Google Gemini API__: Gemini 2.0 Flash vision model
- __Streamlit__: Web interface framework
- __Pillow__: Image processing

## Output Structure

The application organizes output by LLM model and timestamp:

```javascript
output/
├── gpt4omini/
│   └── [timestamp]/
│       ├── page1.md
│       ├── page2.md
│       └── merged_[timestamp].md
├── gemini2flash/
│   └── [timestamp]/
│       ├── page1.md
│       ├── page2.md
│       └── merged_[timestamp].md
└── arch/
    └── [archived outputs]
```

## Purpose of Each IPython Notebook

- __`cost_calc.ipynb`__: Calculates processing costs for different LLM models and resolutions
- __`demo.ipynb`__: Demonstrates basic LLM vision capabilities with image processing
- __`direct_openai.ipynb`__: Shows direct OpenAI API usage patterns for vision models
- __`pdf_handling.ipynb`__: Contains PDF processing utilities and image extraction techniques
- __`wc1.ipynb`__: Working example showing the complete OCR pipeline with vision models

## Use Cases

This application is particularly useful for:

- Converting scanned textbooks to digital format
- Processing multi-page documents with complex layouts
- Preserving document structure and formatting in markdown
- Academic document digitization
- Creating searchable digital archives

