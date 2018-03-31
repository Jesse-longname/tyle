__author__ = 'jonfun8'
import requests

# image_path = "images/ocr_test.png"

key = 'c191bcfdc6ed4e7b85d266d4c830df16'
# image_data = open(image_path, "rb").read()
# headers    = {'Ocp-Apim-Subscription-Key': 'c191bcfdc6ed4e7b85d266d4c830df16',
#               "Content-Type": "application/octet-stream" }
# params     = {'visualFeatures': 'Categories,Description,Color'}
vision_analyze_base = "https://eastus.api.cognitive.microsoft.com/vision/v1.0/"
#
# response   = requests.post(vision_analyze_url,
#                            headers=headers,
#                            params=params,
#                            data=image_data)
#
# response.raise_for_status()
#
# analysis      = response.json()
# image_caption = analysis["description"]["captions"][0]["text"].capitalize()
# print(image_caption)

image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Atomist_quote_from_Democritus.png/338px-Atomist_quote_from_Democritus.png"

ocr_url = vision_analyze_base + 'RecognizeText'
headers  = {'Ocp-Apim-Subscription-Key': key}
params   = {'language': 'unk', 'detectOrientation ': 'true'}
# data     = {'url': image_url}
image_path = "images/reddit.png"

image_data = open(image_path, "rb").read()


#
# data = image_data
# response = requests.post(ocr_url, headers=headers, params=params, json=data)
# response.raise_for_status()
#
# analysis = response.json()
#
# line_infos = [region["lines"] for region in analysis["regions"]]
# word_infos = []
# for line in line_infos:
#     for word_metadata in line:
#         for word_info in word_metadata["words"]:
#             word_infos.append(word_info)
# print (word_infos)

recognize_url = vision_analyze_base + 'RecognizeText'
headers    = {'Ocp-Apim-Subscription-Key': key,
              "Content-Type": "application/octet-stream" }

params   = {'handwriting' : True}
data     = image_data
# data     = {'url': image_url}

response = requests.post(recognize_url, headers=headers, params=params, data=image_data)

response.raise_for_status()
operation_url = response.headers["Operation-Location"]
import time

analysis = {}
while not "recognitionResult" in analysis:
    response_final = requests.get(response.headers["Operation-Location"], headers=headers)
    analysis       = response_final.json()
    time.sleep(1)
result = analysis['recognitionResult']['lines'][0]['text'].replace(" ","")
print (result)