from dotenv import load_dotenv
import os
# Import Langchain modules
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_anthropic import ChatAnthropic
# from langchain.llms import DeepSeek

import base64

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
- Use just plain text and markdown, no HTML tags
- Fully searchable markdown file
- Professional formatting
- No OCR noise/errors
- Semantic markdown structure
- Readable and well-organized
"""

PROMPT_FOR_LAYOUT = """
You ar en OCR expert. I will provide an image of scanned textbook page.
Please analyze this image and provide the bounding box coordinates for all tables, images, graphs, charts, and diagrams. 
For each detected element, return:
1. The element type (table, image, graph, chart, or diagram)
2. The coordinates of its bounding box in [x1, y1, x2, y2] format, where:
   - (x1,y1) is the top-left corner
   - (x2,y2) is the bottom-right corner
   - Coordinates should be in pixels relative to the image dimensions

Please format your response as a JSON object with this structure:
{
  "elements": [
    {
      "type": "table",
      "coordinates": [100, 200, 300, 400]
    },
    {
      "type": "chart",
      "coordinates": [500, 600, 700, 800]
    }
  ]
}
"""

load_dotenv()  # Load variables from .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

chat_models = {'gpt4omini': ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY),
                'gpt4o': ChatOpenAI(model="gpt-4o", api_key=OPENAI_API_KEY),
                'gemini2flash': ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", api_key=GOOGLE_API_KEY)
                }

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

def save_as_markdown(content, file_name, output_path):
    
    trimmed_content = remove_markdown_tags(isolate_markdown(content))
    with open(f"{output_path}/{file_name}.md", 'w', encoding='utf-8') as file:
        file.write(trimmed_content)

def prep_prompt(prompt_template=PROMPT_TEMPLATE, prompt_modifier="spanish"):
    prompt = prompt_template.format(language=prompt_modifier)
    return prompt

def run_llm(img_path,chat_model:str='gpt4omini', prompt=prep_prompt()):
    llm=chat_models[chat_model]
    encoded_image = encode_image(img_path)
    hm=create_image_message(prompt,encoded_image)
    response=llm.invoke([hm])
    
    print(f"processed with {chat_model}")
    return response



# llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)
# llm = ChatOpenAI(model="gpt-4o", api_key=OPENAI_API_KEY)
# llm = ChatOpenAI(model="o1-2024-12-17", api_key=OPENAI_API_KEY)

# llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", api_key=GOOGLE_API_KEY)
# llm = ChatAnthropic(model="claude-3-sonnet-20240229")
# deepseek_model = DeepSeek(api_key="your_deepseek_api_key")







