Supporting_prompt_V2 = '''
# You are a text Question-Answer agent. Your current task is to serve as a reranker. Given a [Claim] that needs to be addressed and a collection of potentially useful [Contexts] related to the claim, along with [Reasoning Steps]  that guide your inference, you need to rank these contexts.
# The format of each piece of context: {"idx":[context index], "title":[context title], "paragraph_text":[content of the context]}
# The [Reasoning Steps] contain A list of Reasoning Steps provided to guide the inference process. Each step contains entities or relationships relevant to the claim.
# you should rank the given contexts according to the following rules:
# 1. How well the context's title or paragraph_text matches the entities or relationships in the reasoning_steps. The better the match, the higher the score.
# 2. The more relevant the context is to the claim, the higher the score is. 
# 3. The more likely the context may contain the answer to the claim, the higher the score is. 
# Please carefully consider the relevance, informativeness, and likelihood of containing the answer when ranking the contexts, and output the top 8 ranked contexts based on the scores..
# You should think step by step and rank the documents above carefully according to the rules.

# Here is a sample of the input format.
# Question: [The claim to be addressed]
# Reasoning Steps: [A list of reasoning steps provided to guide the inference process.]
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
# You are a text Question-Answer agent. Your current task is to serve as a reranker. Given a [Claim] that needs to be addressed and a collection of potentially useful [Contexts] related to the claim, along with [Reasoning Steps]  that guide your inference, you need to rank these contexts.
# The format of each piece of context: {"idx":[context index], "title":[context title], "paragraph_text":[content of the context]}
# The [Reasoning Steps] contain A list of Reasoning Steps provided to guide the inference process. Each step contains entities or relationships relevant to the claim.
# you should rank the given contexts according to the following rules:
# 1. How well the context's title or paragraph_text matches the entities or relationships in the reasoning_steps. The better the match, the higher the score.
# 2. The more relevant the context is to the claim, the higher the score is. 
# 3. The more likely the context may contain the answer to the claim, the higher the score is. 
# Please carefully consider the relevance, informativeness, and likelihood of containing the answer when ranking the contexts, and output the top 6 ranked contexts based on the scores..
# You should think step by step and rank the documents above carefully according to the rules.

# Here is a sample of the input format.
# Question: [The claim to be addressed]
# Reasoning Steps: [A list of reasoning steps provided to guide the inference process.]
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
# You are a text Question-Answer agent. Your current task is to serve as a reranker. Given a [Claim] that needs to be addressed and a collection of potentially useful [Contexts] related to the claim, along with [Reasoning Steps]  that guide your inference, you need to rank these contexts.
# The format of each piece of context: {"idx":[context index], "title":[context title], "paragraph_text":[content of the context]}
# The [Reasoning Steps] contain A list of Reasoning Steps provided to guide the inference process. Each step contains entities or relationships relevant to the claim.
# you should rank the given contexts according to the following rules:
# 1. How well the context's title or paragraph_text matches the entities or relationships in the reasoning_steps. The better the match, the higher the score.
# 2. The more relevant the context is to the claim, the higher the score is. 
# 3. The more likely the context may contain the answer to the claim, the higher the score is. 
# Please carefully consider the relevance, informativeness, and likelihood of containing the answer when ranking the contexts, and output the top 4 ranked contexts based on the scores..
# You should think step by step and rank the documents above carefully according to the rules.

# Here is a sample of the input format.
# Question: [The claim to be addressed]
# Reasoning Steps: [A list of reasoning steps provided to guide the inference process.]
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
# You are a text Question-Answer agent. Your current task is to serve as a reranker. Given a [Claim] that needs to be addressed and a collection of potentially useful [Contexts] related to the claim, along with [Reasoning Steps]  that guide your inference, you need to rank these contexts.
# The format of each piece of context: {"idx":[context index], "title":[context title], "paragraph_text":[content of the context]}
# The [Reasoning Steps] contain A list of Reasoning Steps provided to guide the inference process. Each step contains entities or relationships relevant to the claim.
# you should rank the given contexts according to the following rules:
# 1. How well the context's title or paragraph_text matches the entities or relationships in the reasoning_steps. The better the match, the higher the score.
# 2. The more relevant the context is to the claim, the higher the score is. 
# 3. The more likely the context may contain the answer to the claim, the higher the score is. 
# Please carefully consider the relevance, informativeness, and likelihood of containing the answer when ranking the contexts, and output the top 3 ranked contexts based on the scores..
# You should think step by step and rank the documents above carefully according to the rules.

# Here is a sample of the input format.
# Question: [The claim to be addressed]
# Reasoning Steps: [A list of reasoning steps provided to guide the inference process.]
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

Supporting_prompt_V2_5th = '''
# You are a text Question-Answer agent. Your current task is to serve as a reranker. Given a [Claim] that needs to be addressed and a collection of potentially useful [Contexts] related to the claim, along with [Reasoning Steps]  that guide your inference, you need to rank these contexts.
# The format of each piece of context: {"idx":[context index], "title":[context title], "paragraph_text":[content of the context]}
# The [Reasoning Steps] contain A list of Reasoning Steps provided to guide the inference process. Each step contains entities or relationships relevant to the claim.
# you should rank the given contexts according to the following rules:
# 1. How well the context's title or paragraph_text matches the entities or relationships in the reasoning_steps. The better the match, the higher the score.
# 2. The more relevant the context is to the claim, the higher the score is. 
# 3. The more likely the context may contain the answer to the claim, the higher the score is. 
# Please carefully consider the relevance, informativeness, and likelihood of containing the answer when ranking the contexts, and output the top 2 ranked contexts based on the scores..
# You should think step by step and rank the documents above carefully according to the rules.

# Here is a sample of the input format.
# Question: [The claim to be addressed]
# Reasoning Steps: [A list of reasoning steps provided to guide the inference process.]
# Context: [Collection of relevant contexts]
'''

Supporting_output_prompt_V2_5th = '''
# Please adhere strictly to the following response format,
# Don't output anything else that outside the response format.

# Here is a sample of the output format.
# step-by-step think: your step by step think for rank the contexts
# idx: [index of the highest scoring context, index of the second highest scoring context]

# For example: 
# step-by-step think:1. "Arthur's Magazine" context: It directly relates to the claim as it mentions "Arthur's Magazine" and provides information about its publication period. It is informative and likely contains the answer to the claim. 2. "First for Women" context: This context directly mentions "First for Women," which is part of the claim. It provides information about the magazine, its publisher, and publication date. It is relevant and likely contains the answer to the claim. 3. "Radio City (Indian radio station)" context: Although it does not directly relate to the claim, it provides detailed information about a different topic. However, it might not be as relevant or likely to contain the answer compared to the contexts directly related to the claim. 4. "William Rast" context: This context provides information about a clothing line founded by Justin Timberlake and Trace Ayala. It is informative but not directly relevant to the claim about magazines. 5. "Women's colleges in the Southern United States" context: This context discusses women's colleges in the Southern United States, which is not directly related to the claim about magazines. It is informative but less likely to contain the answer compared to the contexts that directly mention the magazines in question.
# idx: [1,8]
'''
