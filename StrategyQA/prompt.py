Reflexion_prompt_YN = '''
# You are an advanced reasoning agent capable of improving based on self-reflection. 
# You will be given the result and trajectory of a previous reasoning trial, where you were asked to answer a Claim but were unsuccessful in doing so. 
# This is a yes/no question. the Golden Answer is either [yes] or [no]., and your failure due to not correctly determine the Golden Answer of Yes or No (in your response [Answer:] <your answer>).The golden answer is the opposite of what you provided in the previous round (either "yes" or "no").
# Based on the given Claim, Supporting Contexts, and the Trajectory of the previous round of Question-Answer reasoning, diagnose the possible reason for failure or phrasing discrepancy in a few sentences, and devise a new, high-level plan to mitigate similar failures. Pleas use complete sentences.
# Finally, you should provide the opposite of what you provided in the previous round (either "yes" or "no").
# The format of each piece of Supporting context: {"idx":[context index], "paragraph_text":[content of the context]}
'''

Reflexion_output_prompt_YN = '''
# Please adhere strictly to the following response format.
# The format of your response is:   
Reflexion: [Your Plan based on reflection]
Answer: [Your Answer]

For example:
RESPONSE:
Reflexion: The previous reasoning failed because it did not accurately recognize the distinction between the common name "cypress" and the genus "Cupressus." While "Cupressus" is indeed a genus, the term "cypress" can refer to various genera within the family Cupressaceae. The error occurred due to an assumption that "Cupressus" and "cypress" were synonymous in the context of the question. To mitigate similar failures, the plan is to carefully analyze the specific terminology used in the claim and supporting contexts, ensuring that the reasoning is based on precise taxonomic nomenclature rather than common names, which may lead to ambiguity.
Answer: No

'''

Reflexion_prompt = '''
# You are an advanced reasoning agent capable of improving based on self-reflection. 
# You will be given the result and trajectory of a previous reasoning trial, where you were asked to answer a Claim but were unsuccessful in doing so. 
# The golden Answer to the claim is present in the Supporting Contexts, and your failure may be due to not correctly identifying the Golden Answer (in your response [Answer:] <your answer>), or there was a phrasing discrepancy between your Answer and the Golden Answer.
# Based on the given Claim, Supporting Contexts, and the Trajectory of the previous round of Question-Answer reasoning, diagnose the possible reason for failure or phrasing discrepancy in a few sentences, and devise a new, high-level plan to mitigate similar failures. Pleas use complete sentences.
# Finally you should provide your answer to the claim based on your Reflexion
# The format of each piece of Supporting context: {"idx":[context index], "paragraph_text":[content of the context]}
# Reasoning:
# Think step by step with evidence and explanation.
# Generate both answer and step-by-step-reasoning-with-evidence-and-explanation 

'''

Reflexion_output_prompt = '''
# Please adhere strictly to the following response format.
# The format of your response is:   
Reflexion: [Your Plan based on reflection]
Answer: [Your Answer]
Evidence and explanation: [Evidence and explanation used in your think.]
Step by step with evidence and explanation: [Step by step with evidence and explanation].
# Note that:
# In Answer:The answers can be simple [words], [phrases].  You must find the answers directly in these contexts. 

For example:
RESPONSE:
Reflexion: The previous reasoning failed because Robotnik is not a hedgehog; he is a character who is an enemy of Sonic, who is the hedgehog. The error occurred due to a misunderstanding of the character's role within the Sonic the Hedgehog series. To mitigate similar failures, it's important to ensure accurate identification of characters and their roles within their respective series. A high-level plan would include double-checking character identities and their relationships to one another within the context provided.
Answer: Sonic
Evidence and explanation: Jim Cummings is identified as the singer of "A Rather Blustery Day" in context index 9. Context index 4 lists characters voiced by Jim Cummings, which includes Sonic the Hedgehog. Since Sonic is the only hedgehog mentioned in the contexts, he is the correct answer.
Step by step with evidence and explanation:1. The question asks for the hedgehog voiced by the singer of "A Rather Blustery Day."2. Context index 9 confirms that Jim Cummings sang "A Rather Blustery Day."3. Context index 4 lists Sonic the Hedgehog among characters voiced by Jim Cummings.4. Sonic is the hedgehog character in the series, making him the correct answer to the question.

'''

Supporting_prompt_V2 = '''
# You are a text Question-Answer agent, Now you are serving as a reranker. Given a claim to answer and a collection of potentially useful context about the claim.
# The format of each piece of context: {"idx":[context index], "title":[context title], "paragraph_text":[content of the context]}
# you should rank the given contexts according to the following rules:
# 1. The more relevant the context is to the claim, the higher the score is. 
# 2. The more likely the context may contain the answer to the claim, the higher the score is. 
# Please carefully consider the relevance, informativeness, and likelihood of containing the answer when ranking the contexts, and output the top 8 ranked contexts based on the scores..
# You should think step by step and rank the documents above carefully according to the rules.

# Here is a sample of the input format.
# Question: [The claim to be addressed]
# Context: [Collection of relevant contexts]
'''

Supporting_output_prompt_V2 = '''
# Please adhere strictly to the following response format.
# Don't output anything else that outside the response format.

# Here is a sample of the response format.
# step-by-step think: your step by step think for rank the contexts
# idx: [index of the highest scoring context, index of the second highest scoring context, index of the third highest scoring context, index of the fourth highest scoring context, index of the fifth highest scoring context, index of the sixth highest scoring context, index of the seventh highest scoring context, index of the eighth highest scoring context]

# For example: 
# step-by-step think:"Arthur's Magazine" context: It directly relates to the claim as it mentions "Arthur's Magazine" and provides information about its publication period. It is informative and likely contains the answer to the claim. 2. "First for Women" context: This context directly mentions "First for Women," which is part of the claim. It provides information about the magazine, its publisher, and publication date. It is relevant and likely contains the answer to the claim. 3. "Radio City (Indian radio station)" context: Although it does not directly relate to the claim, it provides detailed information about a different topic. However, it might not be as relevant or likely to contain the answer compared to the contexts directly related to the claim. 4. "William Rast" context: This context provides information about a clothing line founded by Justin Timberlake and Trace Ayala. It is informative but not directly relevant to the claim about magazines. 5. "Women's colleges in the Southern United States" context: This context discusses women's colleges in the Southern United States, which is not directly related to the claim about magazines. It is informative but less likely to contain the answer compared to the contexts that directly mention the magazines in question.
# idx: [1,8,2,5,6,7,3,9]
'''

Supporting_prompt_V2_Sec = '''
# You are a text Question-Answer agent, Now you are serving as a reranker. Given a claim to answer and a collection of potentially useful context about the claim.
# The format of each piece of context: {"idx":[context index], "title":[context title], "paragraph_text":[content of the context]}
# you should rank the given contexts according to the following rules:
# 1. The more relevant the context is to the claim, the higher the score is. 
# 2. The more likely the context may contain the answer to the claim, the higher the score is. 
# Please carefully consider the relevance, informativeness, and likelihood of containing the answer when ranking the contexts, and output the top 6 ranked contexts based on the scores..
# You should think step by step and rank the documents above carefully according to the rules.

# Here is a sample of the input format.
# Question: [The claim to be addressed]
# Context: [Collection of relevant contexts]
'''

Supporting_output_prompt_V2_Sec = '''
# Please adhere strictly to the following response format.
# Don't output anything else that outside the response format.

# Here is a sample of the response format.
# step-by-step think: your step by step think for rank the contexts
# idx: [index of the highest scoring context, index of the second highest scoring context, index of the third highest scoring context, index of the fourth highest scoring context, index of the fifth highest scoring context, index of the sixth highest scoring context]

# For example: 
# step-by-step think:"Arthur's Magazine" context: It directly relates to the claim as it mentions "Arthur's Magazine" and provides information about its publication period. It is informative and likely contains the answer to the claim. 2. "First for Women" context: This context directly mentions "First for Women," which is part of the claim. It provides information about the magazine, its publisher, and publication date. It is relevant and likely contains the answer to the claim. 3. "Radio City (Indian radio station)" context: Although it does not directly relate to the claim, it provides detailed information about a different topic. However, it might not be as relevant or likely to contain the answer compared to the contexts directly related to the claim. 4. "William Rast" context: This context provides information about a clothing line founded by Justin Timberlake and Trace Ayala. It is informative but not directly relevant to the claim about magazines. 5. "Women's colleges in the Southern United States" context: This context discusses women's colleges in the Southern United States, which is not directly related to the claim about magazines. It is informative but less likely to contain the answer compared to the contexts that directly mention the magazines in question.
# idx: [1,8,2,5,6,7]
'''

Supporting_prompt_V2_Thd = '''
# You are a text Question-Answer agent, Now you are serving as a reranker. Given a claim to answer and a collection of potentially useful context about the claim.
# The format of each piece of context: {"idx":[context index], "title":[context title], "paragraph_text":[content of the context]}
# you should rank the given contexts according to the following rules:
# 1. The more relevant the context is to the claim, the higher the score is. 
# 2. The more likely the context may contain the answer to the claim, the higher the score is. 
# Please carefully consider the relevance, informativeness, and likelihood of containing the answer when ranking the contexts, and output the top 4 ranked contexts based on the scores..
# You should think step by step and rank the documents above carefully according to the rules.

# Here is a sample of the input format.
# Question: [The claim to be addressed]
# Context: [Collection of relevant contexts]
'''

Supporting_output_prompt_V2_Thd = '''
# Please adhere strictly to the following response format,
# Don't output anything else that outside the response format.

# Here is a sample of the output format.
# step-by-step think: your step by step think for rank the contexts
# idx: [index of the highest scoring context, index of the second highest scoring context, index of the third highest scoring context, index of the fourth highest scoring context]
# For example: 
# step-by-step think:1. "Arthur's Magazine" context: It directly relates to the claim as it mentions "Arthur's Magazine" and provides information about its publication period. It is informative and likely contains the answer to the claim. 2. "First for Women" context: This context directly mentions "First for Women," which is part of the claim. It provides information about the magazine, its publisher, and publication date. It is relevant and likely contains the answer to the claim. 3. "Radio City (Indian radio station)" context: Although it does not directly relate to the claim, it provides detailed information about a different topic. However, it might not be as relevant or likely to contain the answer compared to the contexts directly related to the claim. 4. "William Rast" context: This context provides information about a clothing line founded by Justin Timberlake and Trace Ayala. It is informative but not directly relevant to the claim about magazines. 5. "Women's colleges in the Southern United States" context: This context discusses women's colleges in the Southern United States, which is not directly related to the claim about magazines. It is informative but less likely to contain the answer compared to the contexts that directly mention the magazines in question.
# idx: [1,8,2,5]
'''

Supporting_prompt_V2_4th = '''
# You are a text Question-Answer agent, Now you are serving as a reranker. Given a claim to answer and a collection of potentially useful context about the claim.
# The format of each piece of context: {"idx":[context index], "title":[context title], "paragraph_text":[content of the context]}
# you should rank the given contexts according to the following rules:
# 1. The more relevant the context is to the claim, the higher the score is. 
# 2. The more likely the context may contain the answer to the claim, the higher the score is. 
# Please carefully consider the relevance, informativeness, and likelihood of containing the answer when ranking the contexts, and output the top 3 ranked contexts based on the scores..
# You should think step by step and rank the documents above carefully according to the rules.

# Here is a sample of the input format.
# Question: [The claim to be addressed]
# Context: [Collection of relevant contexts]
'''

Supporting_output_prompt_V2_4th = '''
# Please adhere strictly to the following response format,
# Don't output anything else that outside the response format.

# Here is a sample of the output format.
# step-by-step think: your step by step think for rank the contexts
# idx: [index of the highest scoring context, index of the second highest scoring context, index of the third highest scoring context]
# For example: 
# step-by-step think:1. "Arthur's Magazine" context: It directly relates to the claim as it mentions "Arthur's Magazine" and provides information about its publication period. It is informative and likely contains the answer to the claim. 2. "First for Women" context: This context directly mentions "First for Women," which is part of the claim. It provides information about the magazine, its publisher, and publication date. It is relevant and likely contains the answer to the claim. 3. "Radio City (Indian radio station)" context: Although it does not directly relate to the claim, it provides detailed information about a different topic. However, it might not be as relevant or likely to contain the answer compared to the contexts directly related to the claim. 4. "William Rast" context: This context provides information about a clothing line founded by Justin Timberlake and Trace Ayala. It is informative but not directly relevant to the claim about magazines. 5. "Women's colleges in the Southern United States" context: This context discusses women's colleges in the Southern United States, which is not directly related to the claim about magazines. It is informative but less likely to contain the answer compared to the contexts that directly mention the magazines in question.
# idx: [1,8,2]
'''

Evidence_prompt_golden = '''
# You are a text Question-Answer agent. Given a claim to answer and a collection of potentially useful context about the claim.
# The format of each piece of context: {"idx":[context index], "paragraph_text":[content of the context]}
# Answer can be found directly in the contexts., Your task is to analyze these pieces of contexts, and find the answer to this claim directly in these Contexts.
# Think step by step with evidence and explanation.
# Generate both answer and step-by-step-reasoning-with-evidence-and-explanation 

# Here is a sample of the input format.
# Question: [The claim to be addressed]
# Context: [Collection of relevant contexts]
'''

Evidence_output_prompt_golden = '''
# Please adhere strictly to the following response format.
# The format of your response is:   
# Answer: [Your Answer]
# Evidence and explanation: [Evidence and explanation used in your think.]
# Step by step with evidence and explanation: [Step by step with evidence and explanation].

# Note that Your response can only contain Answer, Evidence and explanation, and Step by step with evidence and explanation!
# In Answer:The answers can be simple [words], [phrases].  You must find the answers directly in these contexts. 
# Your answer should be brief and avoid including narrative statements.
# And then you should write your Evidence and explanation and Step by step with evidence and explanation to show how you come out the answer.

For example:
Answer: Eenasul Fateh
Evidence and explanation: The context provided indicates that Eenasul Fateh is known by the stage name Aladin.
Step by step with evidence and explanation:1. The question asks for the identity of a person known by the stage name Aladin who also worked as a consultant to help organizations improve their performance.2. Context index 7 mentions "Eenasul Fateh, Eenasul Fateh, Bengali, 3 April 1959, Aladin," which directly associates the name Eenasul Fateh with the stage name Aladin.3. The other contexts provided do not contain relevant information about the stage name Aladin or consulting work.4. Therefore, based on the available context, Eenasul Fateh is the person known by his stage name Aladin and helped organizations improve their performance as a consultant.


Example1:
Question: Brown State Fishing Lake is in a country that has a population of how many inhabitants?
Context:{'idx': 0, 'paragraph_text': '9,984, Brown County, U.S., Kansas, 2010, Hiawatha, Brown County, the Kickapoo Indian Reservation of Kansas, the Iowa Reservation of Kansas, Nebraska'}, {'idx': 9, 'paragraph_text': 'Brown County, Kansas, the United States, Brown County State, Hiawatha, Kansas'}, {'idx': 8, 'paragraph_text': 'Kansas, Parsons, Kansas, USA, 1927, vault toilets, McKinley, age 15, the Kansas Department of Wildlife and, Parks'}
Answer: 9,984
Evidence and explanation: All provided contexts mention the population of Brown County, Kansas, where Brown State Fishing Lake is located, as 9,984.
Step by step with evidence and explanation:1. The claim asks for the population of the country where Brown State Fishing Lake is located. 2. Context index 0 mentions Brown County, Kansas, with a population of 9,984. 3. Context index 9 confirms that Brown State Fishing Lake is in Brown County, Kansas, in the United States. 4. Context index 8 also mentions Kansas, USA, with the same population figure. 5. Since all contexts point to Brown County, Kansas, in the United States, and consistently mention the population as 9,984, the answer is that Brown State Fishing Lake is in a country with 9,984 inhabitants.

Example2:
Question: 2014 S/S is the debut album of a South Korean boy group that was formed by who?
Context:{'idx': 5, 'paragraph_text': 'YG Entertainment, 2014, South Korean, August 12, 2014, YG Entertainment'}, {'idx': 1, 'paragraph_text': 'YG Entertainment, Winner, South Korean, 2013, YG Entertainment, 2014, Jinwoo, Seunghoon, Mino, Seungyoon, Taehyun, November 2016'}, {'idx': 7, 'paragraph_text': 'MADTOWN, South Korean, 2014, J. Tune Camp, Moos, Daewon, Lee Geon, Jota, H.O., Mad Town, October 6, 2014, Moos, Buffy, 2013, Madtown, December 22, 2016, MADTOWN, GNI Entertainment, J. Tune Camp'}
Answer: YG Entertainment
Evidence and explanation: The debut album "2014 S/S" is by the South Korean group WINNER, which was formed by YG Entertainment.
Step by step with evidence and explanation:1. The claim asks for the entity that formed the South Korean boy group whose debut album is "2014 S/S".2. Context index 5 provides information that "2014 S/S" is the debut album of the South Korean group WINNER.3. Context index 1 states that WINNER is a South Korean boy group formed by YG Entertainment.4. Therefore, the answer to the claim is that the South Korean boy group with the debut album "2014 S/S" was formed by YG Entertainment.

# Please adhere strictly to the following response format.
# The format of your response is:   
# Answer: [Your Answer]
# Evidence and explanation: [Evidence and explanation used in your think.]
# Step by step with evidence and explanation: [Step by step with evidence and explanation].
# Note that Keep Questions: and Context: out of your response.
'''

Evidence_prompt_golden_YN = '''
# You are a text Question-Answer agent. Given a claim to answer and a collection of potentially useful context about the claim.
# The format of each piece of context: {"idx":[context index], "paragraph_text":[content of the context]}
# This is a yes/no question. Your task is to analyze these pieces of contexts, and answer [yes] or [no].
# Think step by step with evidence and explanation.
# Generate both answer and step-by-step-reasoning-with-evidence-and-explanation 

# Here is a sample of the input format.
# Question: [The claim to be addressed]
# Context: [Collection of relevant contexts]

'''

Evidence_output_prompt_golden_YN = '''
# Please adhere strictly to the following response format.
# In Answer:The answer can only be [yes] or [no]. 
# And then you should write your Evidence and explanation and Step by step with evidence and explanation to show how you come out the answer.

# The format of your response is:   
# Answer: [Your Answer]
# Evidence and explanation: [Evidence and explanation used in your think.]
# Step by step with evidence and explanation: [Step by step with evidence and explanation].

For example:
Answer: Yes
Evidence and explanation: The contexts provided indicate that both Local H and For Against are associated with the United States.
Step by step with evidence and explanation:1. The claim asks if Local H and For Against are both from the United States.2. Context index 5 mentions Local H alongside several American names and the location Zion, Illinois, which is in the United States, dating back to 1987.3. Context index 6 mentions a location in the United States, Lincoln, Nebraska, dated 1984, which is associated with For Against.4. Since both contexts link Local H and For Against to locations within the United States, the answer to the claim is yes, they are both from the United States.

Example1:
Question: Were Scott Derrickson and Ed Wood of the same nationality?
Context:{'idx': 1, 'paragraph_text': 'Scott Derrickson, July 16, 1966, American, Los Angeles, California, Sinister, The Exorcism of Emily Rose, Deliver Us From Evil, 2016, Doctor Strange'}, {'idx': 8, 'paragraph_text': 'Edward Davis Wood Jr., October 10, 1924 –, December 10, 1978, American'}, {'idx': 2, 'paragraph_text': 'Ed Wood, 1994, American, Tim Burton, Johnny Depp, Ed Wood, Wood, Bela Lugosi, Martin Landau, Sarah Jessica Parker, Patricia Arquette, Jeffrey Jones, Lisa Marie, Bill Murray'}
Answer: Yes
Evidence and explanation: Both Scott Derrickson and Ed Wood are described as American in the provided contexts.
Step by step with evidence and explanation:1. The claim asks if Scott Derrickson and Ed Wood were of the same nationality.2. Context index 1 states that Scott Derrickson is an American director.3. Context index 8 describes Ed Wood as an American filmmaker.4. Since both individuals are identified as American, the answer to the claim is yes, they were of the same nationality.

Example2:
Question: Are the Laleli Mosque and Esma Sultan Mansion located in the same neighborhood?
Context:{'idx': 3, 'paragraph_text': 'The Laleli Mosque, Turkish, Laleli Camii, Tulip Mosque, 18th-century, Ottoman, Laleli, Fatih, Istanbul, Turkey'}, {'idx': 8, 'paragraph_text': 'The Esma Sultan Mansion, Turkish, Bosphorus in Ortaköy, Istanbul, Turkey, Esma Sultan, today'}, {'idx': 5, 'paragraph_text': 'Esma, Sultan, 21 March 1873, May 1899, Ottoman, Sultan Abdülaziz, Gevheri Kadın, Salih Bey Svatnba, Muslim'}
Answer: No
Evidence and explanation: The debut album "2014 S/S" is by the South Korean group WINNER, which was formed by YG Entertainment.
Step by step with evidence and explanation:1. The claim asks whether the Laleli Mosque and Esma Sultan Mansion are located in the same neighborhood. 2. Context index 3 states that the Laleli Mosque is located in the "Laleli, Fatih" area of Istanbul. 3. Context index 8 indicates that the Esma Sultan Mansion is located "in Ortaköy" in Istanbul. 4. Since "Fatih" and "Ortaköy" are different neighborhoods in Istanbul, the answer to the claim is that the Laleli Mosque and Esma Sultan Mansion are not located in the same neighborhood.
'''