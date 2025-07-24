import json

def get_Context_List(List_path: str):
    context_list = []
    item_list = []
    # List_path = "./result/SupIdx/distractor/V2/8-4-3_05-20_18-36_result_distractor_test.txt"
    with open(List_path, "r", encoding="utf-8") as file:
        for line in file:
            item_list.append(json.loads(line))
    for item in item_list:
        instance = dict(ID=-1, LIST=[])
        instance["ID"] = item["ID"]
        instance["LIST"] = item["idx"]
        context_list.append(instance)
    return context_list

path = "./result/SupIdx/JSON/Joint-4hop-8-4_result.json"
context_list = get_Context_List(path)
for item in context_list:
    if len(json.loads(item["LIST"])) != 4:
        print(item["LIST"])
        print(item["ID"])