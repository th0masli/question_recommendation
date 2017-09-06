# coding=utf-8


def get_conditions(questions, n):
    questions.sort(key=lambda x: x["similarity"], reverse=True)
    if questions[0]["similarity"] < 50:
        return {}
    num = n
    difficulty, point_id, black, teach_item_type = [], [], [], []
    subject = questions[0]["subject"]
    k = 0
    for question in questions:
        if "knowledge_points" in question and question["knowledge_points"] and k <= 5:
            if question["similarity"] >= 50:
                black.append(question['id'])
            d = question["knowledge_points"][0]["difficulty"]
            p = question["knowledge_points"][0]["point_id"]
            t = question["knowledge_points"][0]["teach_item_type"]
            if d and d not in difficulty:
                difficulty.append(d)
            if p and p not in point_id:
                point_id.append(p)
            if t and t not in teach_item_type:
                teach_item_type.append(t)
            k += 1
        if subject != 0:
            continue
        elif question["subject"] != 0:
            subject = question["subject"]

    conditions = {"difficulty": difficulty, "point_id": point_id, "teach_item_type": teach_item_type, \
             "num": num, "black": black, "subject": subject}

    return conditions


'''
def get_conditions(questions, n):
    num = n
    difficulty, point_id, black, teach_item_type = [], [], [], []
    rank_high, rank_rec = rank_filter(questions, 'high'), rank_filter(questions, 'rec')
    if rank_high:
        subject = rank_high[-1]["subject"]
    elif not rank_high:
        subject = rank_rec[0]["subject"]
    for i in range(len(rank_high)):
        black.append(rank_high[i]['id'])
    for j in range(len(rank_rec)):
        d = rank_rec[j]["knowledge_points"][0]["difficulty"]
        p = rank_rec[j]["knowledge_points"][0]["point_id"]
        t = rank_rec[j]["knowledge_points"][0]["teach_item_type"]
        if d not in difficulty:
            difficulty.append(d)
        if p not in point_id:
            point_id.append(p)
        if t not in teach_item_type:
            teach_item_type.append(t)

    conditions = {"difficulty": difficulty, "point_id": point_id, "teach_item_type": teach_item_type,\
                  "num": num, "black": black, "subject": subject}

    return conditions


def rank_filter(questions, rank):
    questions_ranked = []  # similarity filter
    for i in range(len(questions)):
        if len(questions_ranked) == 5:
            break
        if rank == 'rec':
            if questions[i]['similarity'] < 50 and questions[i]['index_id'] == 0 and questions[i]['knowledge_points']:
                questions_ranked.append(questions[i])
        elif rank == 'high':
            if questions[i]['similarity'] >= 50 and questions[i]['index_id'] == 0:
                questions_ranked.append(questions[i])

    return questions_ranked
'''