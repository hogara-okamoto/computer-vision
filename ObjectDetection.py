import sys
from transformers import pipeline
from PIL import Image, ImageDraw

print("ObjectDetection.py is running")  # To confirm script execution

# Get the filename from the command-line argument
if len(sys.argv) > 1:
    filename = sys.argv[1]
    print(f"File argument received: {filename}")
else:
    print("No file argument passed")
    sys.exit(1)

# Get the labels either from command-line arguments or prompt the user
if len(sys.argv) > 2:
    labels = sys.argv[2:] # Split labels by comma
    labels = [label.strip() for label in labels]  # Strip any extra spaces
    print(f"Labels provided: {labels}")
else:
    # Only prompt for input if no labels were provided in the command-line arguments
    if sys.stdin.isatty():  # Check if input is available (not from Flask subprocess)
        labels = input("Enter the labels you want to detect: ").split(",")
        labels = [label.strip() for label in labels]
    else:
        print("No labels provided and no input available.")
        sys.exit(1)

# Print processing message
print(f"Processing the image {filename} with labels: {labels}")

# Object detection logic
checkpoint = "google/owlv2-base-patch16-ensemble"
detector = pipeline(model=checkpoint, task="zero-shot-object-detection")

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

# Print completion message
print(f"Image saved with detections: {output_filename}")