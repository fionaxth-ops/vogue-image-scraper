import base64
from openai import OpenAI
import glob

BATCH_SIZE = 10


client = OpenAI(
    api_key="AIzaSyBq2G0ETwhOamp3_4JcCwdhuSR84yFm2G8",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Getting the base64 string
image_files = sorted(glob.glob("images/vogue_image_*.jpg"))

# Process in batches to avoid timeouts or payload limits
for i in range(0, len(image_files), BATCH_SIZE):
    batch = image_files[i:i + BATCH_SIZE]
    print(f"\n📦 Processing batch {i//BATCH_SIZE + 1} ({len(batch)} images)...")

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

    print(response.choices[0])
