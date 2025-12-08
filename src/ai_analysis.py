import base64
from openai import OpenAI
import glob
from dotenv import load_dotenv
import os
import json
import re
import time 
from pathlib import Path


BATCH_SIZE = 17
ROOT = Path(__file__).resolve().parents[1]  # go up from src/ to project root
TEMP_FILE_PATH = ROOT / "data" / "temp.jsonl"
IMAGE_PATH = ROOT/ "images"
load_dotenv(ROOT / ".env")


client = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=os.getenv("GEMINI_API_KEY")
)

# Function to encode the image
def encode_image(IMAGE_PATH):
  with open(IMAGE_PATH, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Getting the base64 string
image_files = sorted(IMAGE_PATH.glob("vogue_image_*.jpg"))

# Process in batches to avoid timeouts or payload limits
for i in range(0, len(image_files), BATCH_SIZE):
    batch = image_files[i:i + BATCH_SIZE]
    print(f"\nProcessing batch {i//BATCH_SIZE + 1} ({len(batch)} images)...")

    content = [
        {
            "type": "text",
            "text": """Act as a fashion trend forecaster. Analyze this runway collection for Lemaire, Spring 2026 and provide an output in JSON form of the following (for example) and provide 2-3 values per value array: 
            {
              "show": "Dior SS25",
              "themes": ["romantic minimalism", "architectural silhouettes"],
              "colors": ["soft beige", "sky blue", "charcoal"],
              "materials": ["silk", "denim", "sheer organza"],
              "motifs": ["floral", "geometric"],
              "accessories": ["wide belts", "structured bags"],
              "overall_style": "feminine utility"
            }
            """
        }
    ]

    
    for path in batch:
        base64_image = encode_image(path)
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
        })
        print(path)

    response = client.chat.completions.create(
    model="gemini-2.0-flash",
    messages=[
        {
        "role": "user", 
        "content": content
            }
        ],
    )

    print("response received")

    # Clean the data to extract the JSON
    content = response.choices[0].message.content
    json_str = re.search(r"```json\n(.*?)```", content, re.S).group(1)
    data = json.loads(json_str)

    current_epoch_time = int(time.time())
    data["epoch_timestamp"] = current_epoch_time
    
    json.dumps(data)
    
    # Save in a temp folder 
    with open(TEMP_FILE_PATH, "a") as f:
        f.write(json.dumps(data))
        f.write('\n')
    