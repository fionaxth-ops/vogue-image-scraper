from PIL import Image
import os
from pathlib import Path
from os import listdir

BASE_DIR = Path(__file__).resolve().parent.parent.parent
IMAGES_DIR = BASE_DIR / "images"


def extract_image_metadata(image_path: Path) -> dict:
    """Gets the image metadata 

    Args:
        image_path (Path): Path of the image

    Returns:
        dict: Metadata about the image
    """    
    with Image.open(image_path) as img:
        print( {
            "image_id": image_path.stem,
            "width": img.width,
            "height": img.height,
            "aspect_ratio": round(img.width/img.height, 4),
            "format": img.format,
            "file_size_bytes": os.path.getsize(image_path)
        })
    
def loop_through_images(folder_path: Path): 
    """Loops through images in a folder. 

    Args:
        folder_path (Path): Path of the folder
    """    
    for image in os.listdir(folder_path):
        if image.endswith(".jpg"): 
            extract_image_metadata(folder_path/image)

if __name__ == "__main__": 
    loop_through_images(Path(IMAGES_DIR))