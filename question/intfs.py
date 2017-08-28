# coding=utf-8

# return the description of questions or recommend some questions

import requests
import json
import base64


def choose_interface(value, interface):
    text = question_text(value)

    if interface == 'rec':
        return recommend(text)
    elif interface == 'des':
        return description(text)


# call ocr api
def question_text(value):

    url = 'http://10.10.24.198:9093/api/ocr' # ocr api

    base64_img = base64.b64encode(value.read())

    try:
        data = json.dumps({'subject': 1, 'image_data': base64_img, "with_question_segment": False,
                           "with_visualize_info": False, "formula_or_graphics": False})
        response = requests.post(url, data=data)
        root = json.loads(response.text)
        content = base64.b64decode(root['content'])
        content = json.loads(content)
        return content['app_content']
    except Exception, e:
        print str(e)

    '''url = "http://123.59.40.14:8091/demos" # camera and search
    file = {key: (str(value), value, 'image/jpeg')}
    response = requests.request("POST", url, files=file)

    print response.text

    return response.text'''


def recommend(text):

    url = 'http://10.10.63.68:8080/search/query'

    try:
        data = {"task": "matrix", "keywords": text, "limit": "20", "withoutData": "false"}
        response = requests.post(url, data=data)
        root = json.loads(response.text)
        questions = root['questions']
        questions_filtered = sim_filter(questions)
        questions_cleaned = clean_question(questions_filtered)
        return questions_cleaned, 'questions'
    except Exception, e:
        print str(e)


# call question description api
def description(text):

    url = 'http://10.10.30.220:8000/jiekou_noid'

    try:
        data = json.dumps({'stem': text})
        response = requests.post(url, data=data)
        root = json.loads(response.text)
        return root['ret'], 'label'
    except Exception, e:
        print str(e)


def sim_filter(questions):
    questions_filtered = []  # similarity filter
    for i in range(len(questions)):
        if len(questions_filtered) == 5:
            break
        elif questions[i]['similarity'] < 50:
            questions_filtered.append(questions[i])

    return questions_filtered


def clean_question(questions):
    questions_cleaned = []
    for j in range(len(questions)):
        q = {}
        q['question'] = questions[j]['stem_search']
        q['answer'] = questions[j]['answer']
        q['hint'] = questions[j]['hint']
        questions_cleaned.append(q)

    return questions_cleaned