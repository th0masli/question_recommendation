# coding=utf-8

# return the description of questions or recommend some questions

import requests
import json
import base64
import re


def choose_interface(value, interface):
    text = question_text(value)

    if interface == 'rec':
        return recommend(text)
    elif interface == 'rec0':
        return recommend_0(text)
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
        text = content['app_content']
        return text
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
        data = {"task": "matrix", "keywords": text, "limit": "30", "withoutData": "false"}
        response = requests.post(url, data=data)
        root = json.loads(response.text)
        questions = root['questions']
        questions_filtered = sim_filter(questions)
        questions_cleaned = clean_question(questions_filtered)
        return questions_cleaned, 'questions'
    except Exception, e:
        print str(e)


def recommend_0(text):

    url = 'http://10.10.36.200:8001/classification/'

    try:
        data = json.dumps({'stem': text})
        response = requests.post(url, data=data)
        root = response.text
        print root['classification_result']
        return root['classification_result'], 'questions'
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
        elif questions[i]['similarity'] < 50 and questions[i]['index_id'] == 0:
            questions_filtered.append(questions[i])

    return questions_filtered


def clean_question(questions):
    questions_cleaned = []
    for j in range(len(questions)):
        q = {}
        q['question'] = questions[j]['stem_html']
        q['answer'] = questions[j]['answer']
        q['hint'] = questions[j]['hint']
        questions_cleaned.append(q)

    return questions_cleaned


def html(value):
    text = question_text(value)
    html_data = recommend(text)
    html_data = html_data[0]
    html_data = render_mathquill(html_data)
    text = re.sub('<tex>', '\(', text)
    text = re.sub('</tex>', '\)', text)
    data_info = {'origin': text, 'questions': html_data}

    return data_info


def render_mathquill(data):

    for i in range(len(data)):
        data[i]['answer'] = sub_math(data[i]['answer'])
        data[i]['question'] = sub_math(data[i]['question'])
        data[i]['hint'] = sub_math(data[i]['hint'])

    return data


def sub_math(value):

    value = re.sub('<span class="mathquill-embedded-latex">', '<span class="latex">\(', value)
    value = re.sub('</span>', '\)</span>', value)
    value = re.sub('&amp;lt;', '<', value)
    value = re.sub('&amp;gt;', '>', value)

    value = \
        re.sub('/question\_bank',
               'http://7o4zgy.com2.z0.glb.qiniucdn.com/question_bank',
               value).strip()

    return value