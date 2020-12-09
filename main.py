import streamlit as st
import requests
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import io


st.title('顔認識アプリ')

subscription_key = '33f57e5bd9d94d8fa3910b0da3f4360e'
assert subscription_key

face_api_url = 'https://20201129firstchallenge.cognitiveservices.azure.com/face/v1.0/detect'
uplodeed_file = st.file_uploader('画像を選んでね。',type='jpg')

if uplodeed_file is not None:
    img = Image.open(uplodeed_file)
    with io.BytesIO() as output:
        img.save(output,format='JPEG')
        binary_img = output.getvalue()

    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': subscription_key}

    params = {
        'returnFaceId': 'true',
        'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'
    }

    res = requests.post(face_api_url, params=params,headers=headers, data=binary_img)
    results = res.json()
    for result in results:
        rect = result['faceRectangle']

        #テキストの内容
        text_attributes = result['faceAttributes']
        text_age= str(text_attributes['age'])
        text_gender = text_attributes['gender']

        draw = ImageDraw.Draw(img)
        draw.rectangle([(rect['left'],rect['top']),(rect['left'] + rect['width']),(rect['top'] + rect['height'])],fill=None,outline='green', width=5)
        font = ImageFont.truetype("YuGothL.ttc", size=60)
        draw.text((rect['left'],rect['top']-60), 'age='+text_age, font=font, fill=(255,0,0,128))
        draw.text((rect['left'],rect['top']-120), text_gender, font=font, fill=(255,0,0,128))
    st.image(img,use_column_width=True)
