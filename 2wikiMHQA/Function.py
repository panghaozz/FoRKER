import json

def is_number_empty(answer):
    if answer == "":
        return 0
    else:
        return 1

def is_date_empty(answer_data):
    if all(field == '' for field in [answer_data['day'], answer_data['month'], answer_data['year']]):
        return 0
    else:
        return 10

def is_spans_non_empty(answer):
    if len(answer) > 0:
        return 100
    else:
        return 0

def locate_context(idx: int, context: list):
    for location in range(len(context)):
        if context[location]["idx"] == idx:
            return location

def get_Context_List(List_path:str):
    context_list = []
    # List_path = "./result/SupIdx/distractor/V2/8-4-3_05-20_18-36_result_distractor_test.txt"
    with open(List_path, "r", encoding="utf-8") as file:
        for line in file:
            text = (line.strip())
            if "ID:" in text:
                Item = dict(ID=-1, LIST=[])
                ID_data = int(text.split(":")[1])
                Item["ID"] = ID_data
            if "[" in text and text[0] == "[":
                data = json.loads(text)
                if len(data) == 3:
                    Item["LIST"] = data
                    context_list.append(Item)
    return context_list

def find_best_match(input_text, target_phrases):
    matches = []
    for phrase in target_phrases:
        if phrase in input_text:
            matches.append((phrase, input_text.index(phrase)))

    if not matches:
        return input_text

    # 选择匹配项，可以选择第一个匹配项或其他策略
    best_match = matches[0][0]
    return best_match