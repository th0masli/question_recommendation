# coding=utf-8

# return the description of questions or recommend some questions

import requests
import json
import base64
import re
import condition_rec as crec
import random


def choose_interface(value, interface):
    text = question_text(value)

    if interface == 'old_rec':
        return recommend(text)
    elif interface == 'rec':
        return recommend_conditions(text, 5)
    elif interface == 'des':
        return description(text)
    elif interface == 'test':
        return recommend_0(text)


# call ocr api
def question_text(value):

    url = 'http://10.10.24.198:9093/api/ocr'  # ocr api

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
        data = {"task": "matrix", "keywords": text, "limit": "35", "withoutData": "false"}
        response = requests.post(url, data=data)
        root = json.loads(response.text)
        questions = root['questions']
        questions_filtered = sim_filter(questions)
        questions_cleaned = clean_question(questions_filtered)
        questions_cleaned = render_math(questions_cleaned)
        return questions_cleaned, 'questions', questions  # 3rd is raw questions
    except Exception, e:
        print str(e)


def recommend_conditions(text, num):
    questions_cleaned, k, questions = recommend(text)
    conditions = crec.get_conditions(questions, num)

    if not conditions:
        random.shuffle(questions_cleaned)
        return questions_cleaned, k, questions

    url = 'http://10.2.1.84:8686/item_point/query_item_by_condition'

    headers = {
        'content-type': "application/json",
        'cache-control': "no-cache",
    }

    try:
        data = json.dumps({'app_id': 'xbj', 'app_key': 'wenba', 'conditions': conditions})
        response = requests.post(url, data=data, headers=headers)
        root = json.loads(response.text)
        questions = root['items']
        random.shuffle(questions)
        questions_cleaned = clean_question(questions)
        questions_cleaned = render_math(questions_cleaned)
        return questions_cleaned, 'questions', questions
    except Exception, e:
        print str(e)


# call question description api
def description(text):

    url = 'http://10.10.30.220:8000/jiekou_noid'

    try:
        data = json.dumps({'stem': text})
        response = requests.post(url, data=data)
        root = json.loads(response.text)
        return root['ret'], 'label', root
    except Exception, e:
        print str(e)


# similarity filter
def sim_filter(questions):
    random.shuffle(questions)
    questions_filtered = []
    for i in range(len(questions)):
        if len(questions_filtered) == 5:
            break
        elif questions[i]['similarity'] <= 35 and questions[i]['index_id'] == 0:
            questions_filtered.append(questions[i])

    return questions_filtered


def clean_question(questions):
    questions_cleaned = []
    for j in range(len(questions)):
        q = {}
        if 'stem_html' in questions[j]:
            q['question'] = questions[j]['stem_html']
        elif 'item_content' in questions[j]:
            q['question'] = questions[j]['item_content']
        q['answer'] = questions[j]['answer']
        q['hint'] = questions[j]['hint']
        questions_cleaned.append(q)

    return questions_cleaned


def html(value):
    text = question_text(value)
    # html_data = recommend(text)[0] # ver 1.0
    # html_data = recommend_0(text)[0] # test ver1.1 recommendation
    html_data = recommend_conditions(text, 5)[0]  # ver1.2
    text = re.sub('<tex>', '\(', text)
    text = re.sub('</tex>', '\)', text)
    data_info = {'origin': text, 'questions': html_data}

    return data_info


def render_math(data):

    for i in range(len(data)):
        data[i]['answer'] = sub_math(data[i]['answer'])
        data[i]['question'] = sub_math(data[i]['question'])
        data[i]['hint'] = sub_math(data[i]['hint'])

    return data


def sub_math(value):

    if 'mathquill' in value:
        value = re.sub('<span class="mathquill-embedded-latex">', '<span class="latex">\(', value)
        value = re.sub('</span>', '\)</span>', value)
        value = re.sub('>/\)<', '><', value)

    value = re.sub('&amp;lt;', '<', value)
    value = re.sub('&amp;gt;', '>', value)
    value = re.sub('number', '', value)

    value = re.sub('/question\_bank',
                   'https://wb-qb-qiniu.xueba100.com/question_bank',
                   value).strip()
    value = re.sub('edit',
                   'https://wb-qb-qiniu.xueba100.com/edit',
                   value).strip()
    value = re.sub('/image',
                   'https://wb-qb-qiniu.xueba100.com/image',
                   value).strip()

    return value


def recommend_0(text):

    url = 'http://10.10.36.200:8001/classification/'

    headers = {
        'content-type': "application/json",
        'cache-control': "no-cache",
    }

    try:
        data = json.dumps({'stem': text})
        response = requests.post(url, data=data, headers=headers)
        root = json.loads(response.text)
        classification = trans_temp(root['classification_result'])
        return classification, 'questions', root
    except Exception, e:
        print str(e)


def trans_temp(data):
    struct_data = []
    for i in range(len(data)):
        q = {}
        q['question'] = data[i]
        struct_data.append(q)
    return struct_data