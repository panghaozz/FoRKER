import spacy
from spacy.matcher import PhraseMatcher
import json
import time
from Function import is_number_empty, is_date_empty, is_spans_non_empty, locate_context, get_Context_List

# 加载spaCy的英文模型
nlp = spacy.load("en_core_web_sm")

# 定义提取关键词的函数
def extract_keywords(context, adKeyW: list):
    doc = nlp(context)
    keywords = []

    # 手动添加额外的关键词
    for keyword in adKeyW:
        if keyword in context:
            key_text = "(" + str(keyword) + ")"
            keywords.append(key_text)

    '''
    # 手动添加额外的关键词
    for word in adKeyW:
        keywords.append(word)
     '''

    for entity in doc.ents:
        # 提取特定类型的实体（例如，地名、组织名、日期等）
        if entity.label_ in {"GPE", "ORG", "DATE", "PERSON", "NORP", "FAC", "EVENT", "WORK_OF_ART"}:
            key_text = "(" + str(entity.text) + ")"
            keywords.append(key_text)

    return ', '.join(keywords)

# 定义标准化和格式化函数
def standardize_context(keywords):
    # 在这里可以添加任何额外的标准化逻辑
    return keywords

def knowledge_edit(Context_List:list, adKeyW: str):
    # 定义额外的职称和角色名称
    additional_keywords = []
    additional_keywords.append(str(adKeyW))
    '''
    # 创建PhraseMatcher
    matcher = PhraseMatcher(nlp.vocab)
    patterns = [nlp(text) for text in additional_keywords]
    matcher.add("AdditionalKeywords", None, *patterns)
    '''
    # 处理contexts
    processed_contexts = []
    processed_contexts_no_title = []
    for context in Context_List:
        Temp_Contexts = dict()
        Temp_Contexts_no_title = dict()
        Temp_Contexts["idx"] = context["idx"]
        Temp_Contexts["title"] = context["title"]
        Temp_Contexts_no_title["idx"] = context["idx"]
        keywords = extract_keywords(context["paragraph_text"], additional_keywords)
        standardized = standardize_context(keywords)
        Temp_Contexts["paragraph_text"] = standardized
        Temp_Contexts_no_title["paragraph_text"] = standardized
        processed_contexts.append(Temp_Contexts)
        processed_contexts_no_title.append(Temp_Contexts_no_title)

    return processed_contexts, processed_contexts_no_title

def test():
    Context_List = [{"idx": 3, "title": "A Kiss for Corliss", "paragraph_text": "A Kiss for Corliss is a 1949 American comedy film directed by Richard Wallace and written by Howard Dimsdale. It stars Shirley Temple in her final starring role as well as her final film appearance. It is a sequel to the 1945 film \"Kiss and Tell\". \"A Kiss for Corliss\" was retitled \"Almost a Bride\" before release and this title appears in the title sequence. The film was released on November 25, 1949, by United Artists."}, {"idx": 6, "title": "Shirley Temple", "paragraph_text": "Shirley Temple Black (April 23, 1928 \u2013 February 10, 2014) was an American actress, singer, dancer, businesswoman, and diplomat who was Hollywood's number one box-office draw as a child actress from 1935 to 1938. As an adult, she was named United States ambassador to Ghana and to Czechoslovakia and also served as Chief of Protocol of the United States."}, {"idx": 7, "title": "Kiss and Tell (1945 film)", "paragraph_text": "Kiss and Tell is a 1945 American comedy film starring then 17-year-old Shirley Temple as Corliss Archer. In the film, two teenage girls cause their respective parents much concern when they start to become interested in boys. The parents' bickering about which girl is the worse influence causes more problems than it solves."}]
    adkey = "Chief of Protocol"
    contexts, contexts_notitle = knowledge_edit(Context_List, adkey)
    print(contexts)
    print(contexts_notitle)

def run():
    CurrentTime = time.strftime("%m-%d_%H-%M", time.localtime())
    LEVEL = "distractor"  # {"easy", "hard", "medium"} or {"total"} or {"distractor"}
    TYPE = "test"  # {"train", "test"}
    # MAX_EPOCH = 2
    MAX_ITERATION = 250
    base_path = "./processed_data/hotpotqa/"

    List_path = "./result/SupIdx/distractor/V2/8-4-3_05-20_18-36_result_distractor_test.txt"
    context_dict_list = get_Context_List(List_path)
    result_path = "knowledge editing/" + str(CurrentTime) + "_" + "result_" + str(LEVEL) + "_" + str(TYPE) + ".txt"
    file_path = base_path + str(LEVEL) + "_" + str(TYPE) + ".json"
    datasets = []

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # 解析每一行为一个JSON对象，并添加到列表中
            datasets.append(json.loads(line))

    with open(result_path, 'w', encoding='utf-8') as result_file:
        iters = 0
        while iters < MAX_ITERATION:
            dataset = datasets[iters]
            iters += 1
            Support_Context_Idx_List = []
            DictItem = context_dict_list[iters - 1]
            if DictItem['ID'] == iters:
                Support_Context_Idx_List = DictItem['LIST']

            question = dataset["question_text"]
            context = dataset["contexts"]

            # 现在 data 包含了文件中所有的 JSON 对象
            answer_data = dataset["answers_objects"][0]
            answer_type = is_number_empty(answer_data["number"]) + is_date_empty(
                answer_data["date"]) + is_spans_non_empty(answer_data["spans"])
            if answer_type == 1:
                Right_answer = answer_data['number']
            elif answer_type == 10:
                Right_answer = answer_data['date']
            elif answer_type == 100:
                Right_answer = answer_data['spans'][0]

            Supprt_Context_List = []
            for Sup_Con_Idx in Support_Context_Idx_List:
                Supprt_Context_List.append(context[locate_context(Sup_Con_Idx, context)])
            # print(Supprt_Context_List)

            processed_contexts, processed_contexts_no_title = knowledge_edit(Supprt_Context_List, Right_answer)
            # 记录结果
            result_file.write("#" * 10 + "\n")
            result_file.write(f"ID: {iters}\n\nQuestion: {str(question)}\n\nAnswer: {str(Right_answer)}\n\nOrigin Contexts:\n{Supprt_Context_List[0]}\n{Supprt_Context_List[1]}\n{Supprt_Context_List[2]}\n\nProcessed Contexts:\n{processed_contexts[0]}\n{processed_contexts[1]}\n{processed_contexts[2]}\n\nProcessed Contexts no title:\n{processed_contexts_no_title[0]}\n{processed_contexts_no_title[1]}\n{processed_contexts_no_title[2]}\n")
            result_file.write("#" * 10 + "\n")

            # 输出结果
            print(f"ID: {iters}\nQuestion: {str(question)}\nOrigin Contexts: \n")
            for orig_context in Supprt_Context_List:
                print(orig_context)
            for idx, context in enumerate(processed_contexts, 1):
                print(f"Context {idx}: {context}")

#test()
