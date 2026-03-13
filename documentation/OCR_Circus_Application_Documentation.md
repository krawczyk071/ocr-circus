# OCR-Circus Application Documentation

## Overview

**OCR-Circus** is a sophisticated PDF-to-Markdown conversion application that leverages Large Language Models (LLMs) with vision capabilities to perform Optical Character Recognition (OCR) on scanned documents and convert them into clean, structured markdown files. The application is designed to handle multi-page documents while preserving original formatting, structure, and typography.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Key Features](#key-features)
3. [Technology Stack](#technology-stack)
4. [Installation and Setup](#installation-and-setup)
5. [Usage Guide](#usage-guide)
6. [Core Components](#core-components)
7. [Processing Workflow](#processing-workflow)
8. [Output Structure](#output-structure)
9. [Jupyter Notebooks Reference](#jupyter-notebooks-reference)
10. [Cost Calculation](#cost-calculation)
11. [Use Cases](#use-cases)
12. [Troubleshooting](#troubleshooting)

## Architecture Overview

The OCR-Circus application follows a modular architecture with clear separation of concerns:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   PDF Input     │───▶│  PDF Processing  │───▶│  Image Output   │
│   (Multi-page)  │    │  (PyMuPDF)       │    │   (PNG files)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  LLM Processing │◀───│  Batch Processor │◀───│  Image Loader   │
│  (Vision Models)│    │  (Main Logic)    │    │   (Utilities)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ Markdown Output │◀───│  File Organizer  │◀───│  LLM Responses  │
│ (Per page +     │    │  (File System)   │    │   (Raw Text)    │
│  Merged)        │    └──────────────────┘    └─────────────────┘
└─────────────────┘
```

## Key Features

### Multi-LLM Support
- **OpenAI GPT-4o-mini**: Cost-effective vision model for basic OCR tasks
- **OpenAI GPT-4o**: High-quality vision model for complex documents
- **Google Gemini 2.0 Flash**: Alternative vision model with competitive pricing

### Advanced PDF Processing
- **Page Range Selection**: Process specific pages or page ranges
- **High-Resolution Extraction**: Configurable image quality for better OCR accuracy
- **Multi-Column Layout Support**: Intelligent handling of complex document layouts

### Document Preservation
- **Original Formatting**: Maintains typography, headers, and section hierarchies
- **Table and List Detection**: Properly formats structured content
- **Caption Recognition**: Identifies and preserves image captions and descriptions
- **OCR Artifact Cleanup**: Removes scanning noise and improves text accuracy

### Batch Processing
- **Multi-Page Documents**: Efficiently processes entire documents
- **Parallel Processing**: Optimized for handling large document sets
- **Progress Tracking**: Real-time feedback during processing

### Web Interface
- **Streamlit Application**: User-friendly web interface for document upload and processing
- **Real-time Preview**: View PDF content before processing
- **Download Functionality**: Easy access to processed markdown files

## Technology Stack

### Core Dependencies
- **PyMuPDF (fitz)**: PDF processing and image extraction
- **LangChain**: LLM integration and prompt management
- **OpenAI API**: Access to GPT-4o vision models
- **Google Gemini API**: Access to Gemini 2.0 Flash model
- **Pillow**: Image processing and manipulation
- **Streamlit**: Web interface framework

### Development Tools
- **Jupyter Notebooks**: Development, testing, and demonstration
- **TikToken**: Token counting for cost calculation
- **dotenv**: Environment variable management

## Installation and Setup

### Prerequisites
1. Python 3.11 or higher
2. OpenAI API key (for GPT models)
3. Google API key (for Gemini models)

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/ocr-circus.git
   cd ocr-circus
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   GOOGLE_API_KEY=your_google_api_key_here
   ```

5. **Verify installation:**
   ```bash
   python -c "import fitz; print('PyMuPDF installed successfully')"
   ```

## Usage Guide

### Command Line Usage

#### Basic Usage
```python
from app.app import runner

# Process entire PDF
runner("path/to/document.pdf")

# Process specific page range
runner("path/to/document.pdf", start_page=10, end_page=20)

# Use specific LLM model
runner("path/to/document.pdf", chat_model='gpt4o')
```

#### Advanced Usage
```python
from app.app import lmm_runner
from pathlib import Path

# Process individual images
img_folder = Path("path/to/images")
output_folder = lmm_runner(img_folder, chat_model='gemini2flash')
```

### Web Interface Usage

1. **Start the Streamlit application:**
   ```bash
   streamlit run app/streamlit_app.py
   ```

2. **Upload PDF document:**
   - Navigate to the web interface
   - Use the file uploader to select your PDF
   - Preview the document content

3. **Configure processing options:**
   - Set start and end pages (optional)
   - Select LLM model (default: gpt4omini)

4. **Process and download:**
   - Click "Transform to MD" button
   - Wait for processing to complete
   - Download the generated markdown file

### API Usage

```python
from app.functions_llm import run_llm, prep_prompt
from app.functions_pdf import open_pdf, pdf_select_pages, pdf_doc2screenshots

# Open and prepare PDF
doc = open_pdf("document.pdf")
doc = pdf_select_pages(doc, 1, 5)

# Generate screenshots
img_folder = "temp_images"
pdf_doc2screenshots(doc, img_folder)

# Process with LLM
prompt = prep_prompt("spanish")  # For Spanish documents
response = run_llm("temp_images/page1.png", "gpt4omini", prompt)
```

## Core Components

### Main Application (`app/app.py`)

The main orchestrator that coordinates the entire processing pipeline:

```python
def runner(pdf_path, start_page=None, end_page=None, chat_model='gpt4omini'):
    """Main processing function that handles complete PDF-to-Markdown conversion."""
    # 1. Open and select PDF pages
    doc = open_pdf(pdf_path)
    doc = pdf_select_pages(doc, start_page, end_page)
    
    # 2. Generate screenshots
    img_output_folder = BASE_DIR / "data" / "pdf_screenshots"
    pdf_doc2screenshots(doc, img_output_folder)
    
    # 3. Process with LLM
    out_folder_path = lmm_runner(img_output_folder, chat_model)
    
    # 4. Clean up and merge results
    remove_folder_content(img_output_folder)
    join_markdown_files(out_folder_path)
```

### LLM Integration (`app/functions_llm.py`)

Handles communication with various LLM providers:

- **Model Configuration**: Manages different LLM models and their configurations
- **Prompt Management**: Creates and manages OCR-specific prompts
- **Image Encoding**: Converts images to base64 for LLM processing
- **Response Processing**: Extracts and formats markdown from LLM responses

### PDF Processing (`app/functions_pdf.py`)

Handles all PDF-related operations:

- **Document Opening**: Supports both file paths and file-like objects
- **Page Selection**: Allows processing specific page ranges
- **Image Extraction**: Converts PDF pages to high-resolution PNG images
- **Quality Control**: Configurable zoom factors for image resolution

### Utility Functions (`app/functions.py`)

Provides essential utility functions:

- **File Management**: Folder creation, content removal, and file joining
- **Path Handling**: Cross-platform path operations
- **Time Stamping**: Generates unique timestamps for output organization

## Processing Workflow

### Step 1: Input Processing
1. Accept PDF file (local path or uploaded file)
2. Validate file format and accessibility
3. Optionally select page range for processing

### Step 2: PDF to Image Conversion
1. Open PDF document using PyMuPDF
2. For each selected page:
   - Render page to high-resolution image
   - Save as PNG file with sequential naming
   - Store in temporary directory

### Step 3: LLM Processing
1. For each page image:
   - Encode image to base64 format
   - Create structured prompt for OCR
   - Send to selected LLM model
   - Receive markdown-formatted response

### Step 4: Output Generation
1. Save individual page markdown files
2. Merge all pages into single document
3. Organize output by model and timestamp
4. Clean up temporary files

### Step 5: Result Delivery
1. Provide download links for processed files
2. Display processing summary and statistics
3. Log any errors or warnings encountered

## Output Structure

The application organizes output files in a structured hierarchy:

```
output/
├── gpt4omini/           # OpenAI GPT-4o-mini model outputs
│   └── 250127233317/    # Timestamped processing session
│       ├── ai1_Extracted102_105_p1.md    # Individual page files
│       ├── ai1_Extracted102_105_p2.md
│       ├── ...
│       └── merged_250127233317.md        # Combined document
├── gpt4o/               # OpenAI GPT-4o model outputs
│   └── [timestamp]/
│       ├── page1.md
│       ├── page2.md
│       └── merged_[timestamp].md
├── gemini2flash/        # Google Gemini outputs
│   └── [timestamp]/
│       ├── page1.md
│       ├── page2.md
│       └── merged_[timestamp].md
└── arch/                # Archived outputs
    ├── ai1_Extracted102_105_p1.md
    ├── ai1_Extracted102_105_p1gem.md
    └── ...
```

### File Naming Convention

- **Individual Pages**: `{document_name}_p{page_number}.md`
- **Merged Documents**: `merged_{timestamp}.md`
- **Timestamp Format**: YYMMDDHHMMSS (24-hour format)

## Jupyter Notebooks Reference

### `cost_calc.ipynb`
**Purpose**: Cost calculation and token counting utilities

This notebook provides tools to estimate processing costs for different LLM models and configurations:
- Calculates token usage for prompts and responses
- Estimates costs based on model-specific pricing
- Supports different image resolutions (low, high, auto)
- Includes examples for single and multi-image processing

**Key Functions**:
```python
calculate_openai_cost(prompt_tokens, completion_tokens, image_count, resolution)
count_tokens(text, model="gpt-4")
```

### `demo.ipynb`
**Purpose**: Basic demonstration of LLM vision capabilities

Demonstrates the core functionality of using LLMs for image processing:
- Shows how to encode images for LLM processing
- Demonstrates prompt creation and LLM invocation
- Provides examples of markdown generation from images
- Includes file saving utilities for processed content

**Key Components**:
- Image encoding with base64
- LLM message creation with vision capabilities
- Markdown file generation and saving

### `direct_openai.ipynb`
**Purpose**: Direct OpenAI API usage examples

Shows how to use OpenAI's vision models directly without LangChain abstraction:
- Demonstrates raw API calls to GPT-4 Vision
- Shows proper message formatting for vision models
- Includes error handling and exception management
- Provides examples of different prompt types

**Key Features**:
- Direct API integration patterns
- Error handling for network and API issues
- Proper message structure for vision models

### `pdf_handling.ipynb`
**Purpose**: PDF processing techniques and utilities

Contains comprehensive PDF processing utilities:
- Image extraction from PDF pages
- Page selection and manipulation
- High-resolution screenshot generation
- File organization and cleanup utilities

**Key Functions**:
```python
extract_images_from_pdf(pdf_path, output_folder)
pdf_page_to_image(pdf_path, output_folder, zoom_x, zoom_y)
pdf_select_pages(doc, start_page, end_page)
```

### `wc1.ipynb`
**Purpose**: Working example with vision model integration

A comprehensive working example that demonstrates the complete OCR pipeline:
- Shows integration of all components
- Demonstrates real-world usage patterns
- Includes structured response generation
- Provides complete workflow examples

**Key Features**:
- End-to-end processing example
- Integration of multiple components
- Real document processing examples
- Performance and cost considerations

## Cost Calculation

### Pricing Models

#### OpenAI GPT-4o Models
- **GPT-4o-mini**: $0.03 per 1K prompt tokens, $0.06 per 1K completion tokens
- **GPT-4o**: Higher quality, higher cost (current pricing varies)

#### Google Gemini 2.0 Flash
- **Gemini 2.0 Flash**: Competitive pricing for vision tasks
- **Resolution Impact**: Costs vary based on image resolution settings

### Cost Factors

1. **Image Resolution**:
   - Low resolution: $0.00085 per image
   - High resolution: $0.0085 per image
   - Auto resolution: $0.00255 per image

2. **Token Usage**:
   - Prompt tokens: Based on instruction text length
   - Completion tokens: Based on generated markdown content

3. **Document Complexity**:
   - Text density affects token usage
   - Image content affects processing time
   - Layout complexity affects accuracy requirements

### Cost Optimization

1. **Resolution Selection**: Use lower resolution for text-heavy documents
2. **Page Range**: Process only necessary pages
3. **Model Selection**: Choose appropriate model for document complexity
4. **Batch Processing**: Process multiple documents efficiently

## Use Cases

### Academic Document Digitization
- **Textbooks**: Convert scanned textbooks to searchable digital format
- **Research Papers**: Process academic papers with complex layouts
- **Theses**: Handle lengthy documents with consistent formatting

### Business Document Processing
- **Reports**: Convert business reports to editable formats
- **Manuals**: Process technical documentation
- **Archives**: Digitize historical documents

### Personal Document Management
- **Books**: Convert personal book collections
- **Notes**: Process handwritten or scanned notes
- **Receipts**: Organize financial documents

### Specialized Applications
- **Multi-column Layouts**: Handle newspapers, magazines
- **Mixed Content**: Process documents with text and images
- **Foreign Languages**: Support for various languages (configurable)

## Troubleshooting

### Common Issues

#### PDF Processing Errors
**Problem**: PDF fails to open or process
**Solutions**:
- Verify PDF file is not corrupted
- Check file permissions
- Ensure sufficient disk space for temporary files
- Try different PDF reader software to verify file integrity

#### LLM API Errors
**Problem**: API calls fail or return errors
**Solutions**:
- Verify API keys are correctly set in `.env` file
- Check API usage limits and billing
- Ensure stable internet connection
- Review API documentation for rate limits

#### Image Quality Issues
**Problem**: Poor OCR accuracy or missing content
**Solutions**:
- Increase image resolution (zoom_x, zoom_y parameters)
- Check original PDF quality
- Try different LLM models
- Verify proper lighting in original scans

#### Memory Issues
**Problem**: Application crashes with large documents
**Solutions**:
- Process documents in smaller page ranges
- Increase system memory or swap space
- Close other applications to free memory
- Use command-line interface instead of web interface

### Performance Optimization

#### Processing Speed
- Use GPT-4o-mini for faster, cheaper processing
- Process pages in parallel when possible
- Optimize image resolution for document type
- Use SSD storage for temporary files

#### Accuracy Improvement
- Use higher resolution for complex layouts
- Choose GPT-4o for better accuracy on difficult documents
- Verify prompt instructions are appropriate
- Check original document quality

### Debug Mode

Enable debug logging to troubleshoot issues:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Support and Resources

- **GitHub Issues**: Report bugs and feature requests
- **Documentation**: This file and inline code comments
- **Jupyter Notebooks**: Examples and demonstrations
- **API Documentation**: OpenAI and Google Gemini documentation

## Conclusion

OCR-Circus provides a comprehensive solution for converting scanned PDF documents to structured markdown format using state-of-the-art LLM vision models. The application balances ease of use with powerful features, making it suitable for both casual users and professionals handling large document collections.

The modular architecture allows for easy extension and customization, while the web interface provides an accessible entry point for users without programming experience. The included Jupyter notebooks serve as both documentation and development tools, demonstrating best practices and providing reusable code examples.

For further assistance or to contribute to the project, please visit the GitHub repository or consult the individual component documentation.