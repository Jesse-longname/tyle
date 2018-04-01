from scipy.misc import imsave
import requests
import time

def read_text(ppr_img):
    key = 'c191bcfdc6ed4e7b85d266d4c830df16'
    vision_analyze_base = "https://eastus.api.cognitive.microsoft.com/vision/v1.0/"

    ocr_url = vision_analyze_base + 'RecognizeText'
    headers = {'Ocp-Apim-Subscription-Key': key}
    params = {'language': 'unk', 'detectOrientation ': 'true'}
    image_path = "images/query.png"

    recognize_url = vision_analyze_base + 'RecognizeText'
    headers = {'Ocp-Apim-Subscription-Key': key,
                  "Content-Type": "application/octet-stream" }

    params = {'handwriting' : True}

    # save and load image data
    imsave(image_path, ppr_img)
    image_data = open(image_path, "rb").read()
    
    data = image_data

    response = requests.post(recognize_url, headers=headers, params=params, data=image_data)

    response.raise_for_status()
    operation_url = response.headers["Operation-Location"]

    analysis = {}
    while not "recognitionResult" in analysis:
        response_final = requests.get(response.headers["Operation-Location"], headers=headers)
        analysis       = response_final.json()
        time.sleep(.1)
    if len(analysis['recognitionResult']['lines']) > 0:
        result = analysis['recognitionResult']['lines'][0]['text'].replace(" ","")
    else:
        return None

    return result