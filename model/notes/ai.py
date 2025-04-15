from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
import torch

# Load model and processor
processor = TrOCRProcessor.from_pretrained('microsoft/trocr-base-handwritten')
model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-handwritten')

# Load your handwriting image
image = Image.open("test1.jpeg").convert("RGB")

# Preprocess
pixel_values = processor(images=image, return_tensors="pt").pixel_values

# Predict
generated_ids = model.generate(pixel_values)
text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
print("Recognized text:", text)

from PIL import Image, ImageDraw, ImageFont

def text_to_image(text, font_path='arial.ttf', image_size=(800, 200), font_size=40):
    # Create blank image
    img = Image.new('RGB', image_size, color='white')
    d = ImageDraw.Draw(img)

    # Draw text
    d.text((10, 50), text, fill=(0, 0, 0))

    img.save('output_image.png')
    return img

# Example usage
text_to_image("Your recognized text here", font_path="path/to/font.ttf")
