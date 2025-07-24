import json

context_list = []
List_path = "result/SupIdx/distractor/V2/8-4-3-joint_06-04_15-45_result_distractor_test.txt"
with open(List_path, "r", encoding="utf-8") as file:
    for line in file:
        text = (line.strip())
        if "ID:" in text:
            Item = dict(ID=-1, GolenList=[], LIST=[])
            ID_data = int(text.split(":")[1])
            Item["ID"] = ID_data
        if "golden idx: " in text:
            golden_data = json.loads(text.split(":")[1])
            Item["GoldenList"] = golden_data
        if "[" in text and text[0] == "[":
            data = json.loads(text)
            if len(data) == 3:
                Item["LIST"] = data
                context_list.append(Item)

print(len(context_list))
goal = 0
for iters in range(len(context_list)):
    if context_list[iters]["ID"] != iters + 1:
        print(context_list[iters]["ID"], iters)
        break
    for golden_idx in context_list[iters]["GoldenList"]:
        if golden_idx in context_list[iters]["LIST"]:
            goal += 1
print(f"最终得分{goal / 1000 * 100}%")
