from dotenv import load_dotenv
import os
# Import Langchain modules
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.messages import HumanMessage
import base64

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    
def create_image_message(instruction,encoded_image):
    message = HumanMessage(
        content=[
            {"type": "text", "text": instruction}, # Use the dynamic instruction
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{encoded_image}"}},
        ]
    )
    return message

def isolate_markdown(text):
    start_tag = "```markdown"
    end_tag = "```"
    
    start_index = text.find(start_tag)
    if start_index != -1:
        text = text[start_index:]
    
    end_index = text.rfind(end_tag)
    if end_index != -1:
        text = text[:end_index + len(end_tag)]
    
    return text

def remove_markdown_tags(text):
    start_tag = "```markdown"
    end_tag = "```"
    
    start_index = text.find(start_tag)
    if start_index != -1:
        text = text[:start_index] + text[start_index + len(start_tag):]
    
    end_index = text.rfind(end_tag)
    if end_index != -1:
        text = text[:end_index] + text[end_index + len(end_tag):]
    
    return text

def save_as_markdown(content, file_name):
    
    trimmed_content = remove_markdown_tags(isolate_markdown(content))
    
    with open(f"../output/{file_name}.md", 'w', encoding='utf-8') as file:
        file.write(trimmed_content)

def run_llm(img_path):
    prompt=PROMPT_TEMPLATE.format(language="spanish")
    encoded_image = encode_image(img_path)
    hm=create_image_message(prompt,encoded_image)
    response=llm.invoke([hm])
    return response

load_dotenv()  # Load variables from .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)

PROMPT_TEMPLATE = """
You are an expert PDF OCR and markdown conversion assistant.
Given an image of full page scanned {language} textbook:
1. Perform full OCR processing
2. Preserve original document structure
3. Convert to clean markdown
4. Maintain:
   - Original formatting
   - Section hierarchies
   - Typography distinctions
   - Tables and lists
5. Clean up OCR artifacts
6. Ensure maximum text accuracy
7. Handle multi-column layouts intelligently
8. Detect and properly format headers, paragraphs, captions

Output requirements:
- Fully searchable markdown file
- Professional formatting
- No OCR noise/errors
- Semantic markdown structure
- Readable and well-organized
"""





