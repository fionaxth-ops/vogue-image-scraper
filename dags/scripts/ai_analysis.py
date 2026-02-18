import base64
from openai import OpenAI
import glob
from dotenv import load_dotenv
import os
import json
import re
import time 
import itertools

from pathlib import Path

REQUEST_DELAY_SECONDS = 3 
BATCH_SIZE = 10
ROOT = Path(__file__).resolve().parents[2]  # go up from src/ to project root
load_dotenv()

client = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=os.getenv("GEMINI_API_KEY")
)

# Function to encode the image
def encode_image(images_path: Path):
    with open(images_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def image_analysis(images_path: Path, temp_file_path: Path):
    """Analyze images in batches using the Gemini model and append JSONL results.

    Scans `images_path` for files named `vogue_image_*.jpg`, encodes each
    image to base64 and sends images to the Gemini model in batches. The
    function extracts the JSON response from the model, adds an
    `epoch_timestamp`, and appends each result as a separate JSON line to
    `temp_file_path`.

    Args:
        images_path (Path): Directory containing image files to analyze.
        temp_file_path (Path): Output file path where JSONL results are appended.

    Returns:
        None
    """

    print("IMAGES_PATH:", images_path)
    print("Exists?", images_path.exists())
    print("Files:", list(images_path.glob("*")))

    image_files = sorted(images_path.glob("vogue_image_*.jpg"))

    # Process in batches to avoid timeouts or payload limits
    for i, batch in enumerate(itertools.batches(image_files, BATCH_SIZE)):
        print(f"\nProcessing batch {i + 1} ({len(batch)} images)...")

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
        model="gemini-2.5-flash",
        messages=[
            {
            "role": "user", 
            "content": content
                }
            ],
        )

        print("response received")
        time.sleep(REQUEST_DELAY_SECONDS)

        # Clean the data to extract the JSON
        content = response.choices[0].message.content
        json_str = re.search(r"```json\n(.*?)```", content, re.S).group(1)
        data = json.loads(json_str)

        current_epoch_time = int(time.time())
        data["epoch_timestamp"] = current_epoch_time
        
        json.dumps(data)
        
        # Create parent directory if it doesn't exist, then append to file
        temp_file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(temp_file_path, "a") as f:
            f.write(json.dumps(data))
            f.write('\n')

# Code to test the script individually
if __name__ == "__main__": 
    BASE_PATH = Path(__file__).resolve().parent.parent.parent
    IMAGES_PATH = BASE_PATH / "images"
    TEMP_FILE_PATH = BASE_PATH / "data" / "temp.jsonl"

    image_analysis(IMAGES_PATH, TEMP_FILE_PATH)

