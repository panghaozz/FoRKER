import json

context_list = []
List_path = "./result/SupIdx/distractor/V2/8-4-3_05-20_18-36_result_distractor_test.txt"
with open(List_path, "r", encoding="utf-8") as file:
    for line in file:
        text = (line.strip())
        if "ID:" in text:
            Item = dict(ID=-1, LIST=[])
            ID_data = int(text.split(":")[1])
            Item["ID"] = ID_data
        if "[" in text and text[0] == "[":
        #if "idx:" in text and text[0] == "i":
            #data = json.loads(text.split(":")[1])
            data = json.loads(text)
            if len(data) == 3:
                Item["LIST"] = data
                context_list.append(Item)
print(context_list)
print(len(context_list))


for i in range(236):
    if i  != context_list[i]["ID"] -1:
        print(f"error! {i + 1}")
        break

