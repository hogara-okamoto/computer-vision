import sys
import json  # Import the JSON module
from transformers import pipeline
import torch
from PIL import Image, ImageDraw

print("Using device:", "GPU" if torch.cuda.is_available() else "CPU", file=sys.stderr)
print("ObjectDetection.py is running", file=sys.stderr)

# Get the filename from the command-line argument
if len(sys.argv) > 1:
    filename = sys.argv[1]
    print(f"File argument received: {filename}", file=sys.stderr)
else:
    print("No file argument passed")
    sys.exit(1)

# Get the labels either from command-line arguments or prompt the user
if len(sys.argv) > 2:
    labels = sys.argv[2:] # Split labels by comma
    labels = [label.strip() for label in labels]  # Strip any extra spaces
    print(f"Labels provided: {labels}", file=sys.stderr)
else:
    # Use default labels
    labels = ['python', 'ObjectDetection.py', filepath, 'Lion', 'Elephant', 'Giraffe', 'Kangaroo', 'zebra', 'Panda', 'Tiger', 'cat', 'dog', 'person'],
    print(f"No labels provided. Using default labels: {labels}", file=sys.stderr)

# Print processing message
print(f"Processing the image {filename} with labels: {labels}", file=sys.stderr)

# Object detection logic
device = 0 if torch.cuda.is_available() else -1
checkpoint = "google/owlv2-base-patch16-ensemble"
detector = pipeline(model=checkpoint, task="zero-shot-object-detection", device=device)

# Open the image file
image = Image.open(filename)

# Perform detection
predictions = detector(
    image,
    candidate_labels=labels,
)

# Draw bounding boxes and labels on the image
draw = ImageDraw.Draw(image)
for prediction in predictions:
    box = prediction["box"]
    label = prediction["label"]
    score = prediction["score"]

    xmin, ymin, xmax, ymax = box.values()
    draw.rectangle((xmin, ymin, xmax, ymax), outline="red", width=1)
    draw.text((xmin, ymin), f"{label}: {round(score, 2)}", fill="black")

# Save the processed image
output_filename = f"{filename.split('.')[0]}_detection.png"
image.save(output_filename)

# Print the JSON result (this is critical for your app.py to work)
print(json.dumps(predictions))

# Exit successfully
sys.exit(0)