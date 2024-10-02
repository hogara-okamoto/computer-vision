## Computer vision

When you upload a photo of a single animal or a group of animals, this program detects the animals and returns an image with their names identified. To run the program locally, use npm run dev and python app.py

- ImageUploader.tsx   
This is the homepage. The page.tsx in the app directory displays this file. This will be run on http://localhost:3000

- app.py  
This is the Frask file. This file passes and receives an image from and to ImageUploader.tsx to process the image in ObjectDetection.py. This will be run on http://127.0.0.1:5000

- ObjectDetection.py  
This is the object detetion file. This file uses "google/owlv2-base-patch16-ensemble" as a check point. This file currently detect 10 animals and a person.


## Room for improvement

1. Using Google's API takes time, so it would be better to use a model that has been trained locally.

2. Google's current API significantly reduces identification accuracy when animals overlap.

3. As the number of animals to be identified increases, the object detection time increases. GPU might be able to solve this problem.