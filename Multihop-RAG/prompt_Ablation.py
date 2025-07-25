E2G_prompt = '''
# You are a text Question-Answer agent. Given a claim to answer and a collection of potentially useful context about the claim.
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
# You are a text Question-Answer agent. Given a claim to answer and a collection of potentially useful context about the claim.
# This is a yes/no question.  Answer [yes] or [no].
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
# You are a text Question-Answer agent. Given a claim to answer and a collection of potentially useful context about the claim.
#  Think step by step to come out the answer.
'''

CoT_output_prompt = '''
# Please adhere strictly to the following response format.
# The format of your response is: 
Answer: [Your answer]
Step-by-step reasoning: [Your Step-by-step reasoning ]
'''

CoT_prompt_YN = '''
# You are a text Question-Answer agent. Given a claim to answer and a collection of potentially useful context about the claim.
# This is a yes/no question.  Answer [yes] or [no].
#  Think step by step to come out the answer.
'''

CoT_output_prompt_YN = '''
# Please adhere strictly to the following response format.
# The format of your response is: 
Answer: [Your answer]
Step-by-step reasoning: [Your Step-by-step reasoning ]
'''

No_CoE_prompt = '''
# You are a text Question-Answer agent. Given a claim to answer and a collection of potentially useful context about the claim.
# The format of each piece of context: {"idx":[context index], "title":[title of the context], "paragraph_text":[content of the context]}
#  Find the answer to this claim.
'''

No_CoE_output_prompt = '''
# Please adhere strictly to the following response format.
# The format of your response is: 
Answer: [Your answer]
'''

No_CoE_prompt_KE = '''
# You are a text Question-Answer agent. Given a claim to answer and a collection of potentially useful context about the claim.
# The format of each piece of context: {"idx":[context index], "title":[title of the context], "paragraph_text":[content of the context]}
# Your task is to analyze these pieces of contexts, and find the answer to this claim directly in these Contexts.
'''

No_CoE_output_prompt_KE = '''
# Please adhere strictly to the following response format.
# The format of your response is: 
Answer: [Your answer]
'''

No_CoE_prompt_YN = '''
# You are a text Question-Answer agent. Given a claim to answer and a collection of potentially useful context about the claim.
# The format of each piece of context: {"idx":[context index], "title":[title of the context], "paragraph_text":[content of the context]}
#  Find the answer to this claim.
'''

No_CoE_output_prompt_YN = '''
# Please adhere strictly to the following response format.
# The format of your response is: 
Answer: [Your answer]
'''