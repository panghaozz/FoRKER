E2G_prompt = '''
# You are a text Question-Answer agent. Given a claim to answer and a collection of potentially useful context about the claim, along with reasoning steps that guide your inference.
# The format of each piece of context: {"idx":[context index], "title":[title of the context], "paragraph_text":[content of the context]}
# The [Reasoning Steps] contain A list of Reasoning Steps provided to guide the inference process.
#  Think step by step with evidence and explanation.
#  Generate both answer and step-by-step-reasoning-with-evidence-and-explanation 
'''
E2G_Output_prompt = '''
# Please adhere strictly to the following response format.
# The format of your response is: 
# Answer: [Your answer]
# Evidence and explanation:[Your Evidence and explanation]
# Step-by-step reasoning with evidence and explanation: [Your Step-by-step reasoning with evidence and explanation]
'''

E2G_prompt_YN = '''
# You are a text Question-Answer agent. Given a claim to answer and a collection of potentially useful context about the claim, along with reasoning steps that guide your inference..
# The format of each piece of context: {"idx":[context index], "title":[title of the context], "paragraph_text":[content of the context]}
# The [Reasoning Steps] contain A list of Reasoning Steps provided to guide the inference process.
# This is a yes/no question. Your task is to analyze these pieces of contexts, and answer [yes] or [no].
# Think step by step with evidence and explanation.
# Generate both answer and step-by-step-reasoning-with-evidence-and-explanation 
'''

E2G_Output_prompt_YN = '''
# Please adhere strictly to the following response format.
# The format of your response is:   
# Answer: [Your Answer]
# Evidence and explanation: [Evidence and explanation used in your think.]
# Step by step with evidence and explanation: [Step by step with evidence and explanation].
'''

CoT_prompt = '''
# You are a text Question-Answer agent. Given a claim to answer and a collection of potentially useful context about the claim, along with reasoning steps that guide your inference.
# The format of each piece of context: {"idx":[context index], "title":[title of the context], "paragraph_text":[content of the context]}
# The [Reasoning Steps] contain A list of Reasoning Steps provided to guide the inference process.
#  Think step by step to come out the answer.
'''

CoT_output_prompt = '''
# Please adhere strictly to the following response format.
# The format of your response is: 
Answer: [Your answer]
Step-by-step reasoning: [Your Step-by-step reasoning ]
'''


CoT_prompt_YN = '''
# You are a text Question-Answer agent. Given a claim to answer and a collection of potentially useful context about the claim, along with reasoning steps that guide your inference..
# The format of each piece of context: {"idx":[context index], "title":[title of the context], "paragraph_text":[content of the context]}
# The [Reasoning Steps] contain A list of Reasoning Steps provided to guide the inference process.
# This is a yes/no question. Your task is to analyze these pieces of contexts, and answer [yes] or [no].
#  Think step by step to come out the answer.
'''

CoT_output_prompt_YN = '''
# Please adhere strictly to the following response format.
# The format of your response is: 
Answer: [Your answer]
Step-by-step reasoning: [Your Step-by-step reasoning ]
'''


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