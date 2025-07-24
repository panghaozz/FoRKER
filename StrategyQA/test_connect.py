from openai import OpenAI
import httpx
from time import sleep

client = OpenAI(
    base_url="https://xiaoai.plus/v1",
    api_key="sk-inNndrUrn8S4hfpy328c83E091364cF1B743Ee6d1dA9818f",
    http_client=httpx.Client( base_url="https://xiaoai.plus/v1", follow_redirects=True,),
)

set_prompt = '''# 你多少钱一个月'''
set_prompt_R = '''
# You are an advanced reasoning agent capable of improving based on self-reflection. 
# You will be given the result and trajectory of a previous reasoning trial, where you were asked to answer a Claim but were unsuccessful in doing so. 
# The golden Answer to the claim is present in the Supporting Contexts, and your failure may be due to not correctly identifying the Golden Answer (in your response [Answer:] <your answer>), or there was a phrasing discrepancy between your Answer and the Golden Answer.
# Based on the given Claim, Supporting Contexts, and the Trajectory of the previous round of Question-Answer reasoning, diagnose the possible reason for failure or phrasing discrepancy in a few sentences, and devise a new, high-level plan to mitigate similar failures. Pleas use complete sentences.
# Finally you should provide your answer to the claim based on your Reflexion
# The format of each piece of Supporting context: {"idx":[context index], "paragraph_text":[content of the context]}
# Reasoning:
# Think step by step with evidence and explanation.
# Generate both answer and step-by-step-reasoning-with-evidence-and-explanation 

Question: Which Australian city founded in 1838 contains a boarding school opened by a Prime Minister of Australia and named after a school in London of the same name.
Supporting Contexts:{'idx': 9, 'title': 'Westminster School, Adelaide', 'paragraph_text': 'Westminster School is an independent, Uniting Church, Early Learning to Year 12, coeducational, day and boarding school located at Marion, South Australia, 12 km south of Adelaide. Founded as a Methodist day and boarding school for boys, the school was opened by the Prime Minister Robert Menzies in 1961 and is named after Westminster School in London. The school became co-educational in 1978, and has a current enrolment of around 1150 students.'} {'idx': 0, 'title': 'Marion, South Australia', 'paragraph_text': 'Marion is a suburb in the City of Marion in Adelaide around 10 km south-west of the CBD. Founded as a rural village in 1838 on the banks of the Sturt River, Marion was found to have rich soil and the population expanded rapidly. Colonel William Light laid out the plan for the village, as he had done with the City of Adelaide itself.'} {'idx': 8, 'title': 'Sainik School Balachadi, Jamnagar', 'paragraph_text': 'The Sainik School Balachadi ("Hindi: सैनिक शाला बालाचडी" ), Jamnagar, Gujarat, is one of the Top Sainik School in the Chain of 26 Sainik Schools in India. It is one of the boarding school for public education in Gujarat.It was established in July 1961 by then the Honorable Prime Minister Sri Lal Bahadur Shastri.It is an elite English medium, fully residential boarding school for boys providing Premium public school education with a Military bias up to 10+2 stage as per the Central Board of Secondary Education.The Chain of Sainik Schools in India was established as a prime focus of strengthening the Armed Forces and All India Services IAS & IPS, and other fields of Public services. The School is Located at a distance of 32\xa0km from the main city of Jamnagar alongside a coastal area. The campus facing the Gulf of Kutch is encompassed with a Bungalow of The Ruler of Nawanagar Maharaja Jam Shaheb Digvijaysinhji Ranjitsinhji, Sachana Ship Breaking Yard and a natural sea beach.'}
Previous round's results and trajectory: Answer: Adelaide
Evidence and explanation: The context provided indicates that the City of Marion, which is part of Adelaide, was founded in 1838 and contains Westminster School, a boarding school opened by Prime Minister Robert Menzies.
Step by step with evidence and explanation:
1. The claim asks for the Australian city founded in 1838 that contains a boarding school named after a school in London.
2. Context index 0 states that the City of Marion was founded in 1838 and is associated with the City of Adelaide.
3. Context index 9 mentions Westminster School in Marion, South Australia, which is associated with Adelaide, opened by Robert Menzies in 1961, and named after Westminster School in London.
4. Therefore, the answer is Adelaide, as it is the city that encompasses Marion, where the school named after the London school is located.

# Please adhere strictly to the following response format.
# The format of your response is:   
Reflexion: [Your Plan based on reflection]
Answer: [Your Answer]
Evidence and explanation: [Evidence and explanation used in your think.]
Step by step with evidence and explanation: [Step by step with evidence and explanation].
# Note that:
# In Answer:The answers can be simple [words], [phrases].  You must find the answers directly in these contexts. 

'''
set_prompt_RQA = '''
# Task:
# You are a text Question-Answer agent. You will be given a claim to answer and a collection of potentially useful contexts about the claim.
# Each piece of context is formatted as: {"idx":[context index], "paragraph_text":[content of the context]}.
# The answer can be found directly in these contexts.
# You have attempted to answer this claim before and failed. The following reflections give a plan to avoid failing to answer the claim in the same way you did previously. Use them to improve your strategy of correctly answering the given claim.
# Your task is to analyze these pieces of context and your Reflexion, and find the answer to this claim directly in these contexts.
# Reasoning:
# Think step by step with evidence and explanation.
# Generate both answer and step-by-step-reasoning-with-evidence-and-explanation 

# Here is a sample of the input format.
# Question: [The claim to be addressed]
# Context: [Collection of relevant contexts]

# Please adhere strictly to the following response format.
# The format of your response is:   
# Answer: [Your Answer]
# Evidence and explanation: [Evidence and explanation used in your think.]
# Step by step with evidence and explanation: [Step by step with evidence and explanation].

# Note that Your response can only contain Answer, Evidence and explanation, and Step by step with evidence and explanation!
# In Answer:The answers can be simple [words], [phrases].  You must find the answers directly in these contexts. 
# Your answer should be brief and avoid including narrative statements.
# And then you should write your Evidence and explanation and Step by step with evidence and explanation to show how you come out the answer.

Question: This singer of A Rather Blustery Day also voiced what hedgehog?
Context: {'idx': 4, 'paragraph_text': "Sonic, James Jonah Cummings, November 3, 1952, American, Darkwing Duck, Robotnik, Sonic the Hedgehog, Pete, Winnie the Pooh, Tigger, the Tasmanian Devil, Disney, DreamWorks, Aladdin, The Lion King, Balto, The Road to El Dorado, Shrek, The Princess and the Frog, Icewind Dale, Fallout, Baldur's Gate, Mass Effect 2, Splatterhouse"}{'idx': 9, 'paragraph_text': 'A Rather Blustery Day, Walt Disney, Winnie the Pooh and the Blustery Day, Robert & Richard Sherman, Jim Cummings, Pooh'}{'idx': 7, 'paragraph_text': 'Winnie, the Blustery Day, 1968, Winnie, eighth, The House at Pooh Corner, A. A. Milne, Walt Disney Productions, Buena Vista Distribution Company, December 20, 1968, The Horse in the Gray Flannel Suit, Winnie, Pooh, 1977, The Many Adventures of Winnie the Pooh, Richard M. Sherman, Robert B. Sherman, Walt Disney'}
Reflexion: The previous reasoning failed because Robotnik is not a hedgehog; he is a character who is an adversary of Sonic, who is the hedgehog in the series. The golden answer should be Sonic the Hedgehog, as he is the only hedgehog mentioned in the supporting contexts and is a character associated with Jim Cummings. To mitigate similar failures, the plan should include a step to verify the accuracy of character roles and relationships within the context provided, ensuring that the answer aligns with the specific details of the question. Additionally, it's important to cross-reference all supporting contexts to confirm the answer before finalizing it.
'''
set_prompt_RYN = '''
# You are an advanced reasoning agent capable of improving based on self-reflection. 
# You will be given the result and trajectory of a previous reasoning trial, where you were asked to answer a Claim but were unsuccessful in doing so. 
# This is a yes/no question. the Golden Answer is either [yes] or [no]., and your failure due to not correctly determine the Golden Answer of Yes or No (in your response [Answer:] <your answer>).The golden answer is the opposite of what you provided in the previous round (either "yes" or "no").
# Based on the given Claim, Supporting Contexts, and the Trajectory of the previous round of Question-Answer reasoning, diagnose the possible reason for failure or phrasing discrepancy in a few sentences, and devise a new, high-level plan to mitigate similar failures. Pleas use complete sentences.
# Finally, you should provide the opposite of what you provided in the previous round (either "yes" or "no").
# The format of each piece of Supporting context: {"idx":[context index], "paragraph_text":[content of the context]}

Question: Are both Cypress and Ajuga genera?
Supporting Contexts:{'idx': 2, 'title': 'Ajuga', 'paragraph_text': 'Ajuga , also known as bugleweed, ground pine, carpet bugle, or just bugle, is a genus of 40 species annual and perennial herbaceous flowering plantsin the mint family Lamiaceae, with most species native to Europe, Asia, and Africa, but also two species in southeastern Australia. They grow to 5–50 cm tall, with opposite leaves.'}{'idx': 1, 'title': 'Cupressus', 'paragraph_text': 'The genus Cupressus is one of several genera within the family Cupressaceae that have the common name cypress; for the others, see cypress. It is considered a polyphyletic group. Based on genetic and morphological analysis, the "Cupressus" genus is found in the Cupressoideae subfamily. The common name comes from Old French "cipres" and that from Latin "cyparissus", which is the latinisation of the Greek κυπάρισσος ("kypárissos").'}{'idx': 5, 'title': 'Ajugeae', 'paragraph_text': 'Ajugeae is a tribe of the Teucrioideae subfamily of the family Lamiaceae and might contain the genera "Acrymia" , "Ajuga" , "Cymaria" , "Garrettia" , "Holocheila" .'}
Previous round's results and trajectory: Answer: Yes
Evidence and explanation: The context provided indicates that both Cypress and Ajuga are referred to in a taxonomic context, suggesting they are both genera.
Step by step with evidence and explanation:
1. The claim asks if Cypress and Ajuga are both genera.
2. Context index 1 mentions "Cupressus," which is the genus for Cypress trees, and associates it with the family "Cupressaceae" and subfamily "Cupressoideae."
3. Context index 2 refers to "Ajuga," also known as carpet bugle, and associates it with the family "Lamiaceae," which is indicative of its genus status.
4. Context index 5 lists "Ajuga" within a group that includes other genera such as "Acrymia" and "Garrettia," further confirming its status as a genus.
5. Since both "Cupressus" and "Ajuga" are listed with taxonomic ranks and associated with specific families, it can be concluded that they are indeed both genera. Therefore, the answer to the question is yes.

# Please adhere strictly to the following response format.
# The format of your response is:   
Reflexion: [Your Plan based on reflection]
Answer: [Your Answer]
'''
try:
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": set_prompt_R},
        ],
        temperature=0,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    response = completion.choices[0].message.content.strip()
    print(f"RESPONSE:\n" + response)
    resp_text_list = response.split("\n")
    filtered_list = [element for element in resp_text_list if element.strip()]

except Exception as e:
    print(e)
    sleep(1)
