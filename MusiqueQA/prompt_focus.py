Supporting_prompt_V2_8th = '''
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

Supporting_output_prompt_V2_8th = '''
# Please adhere strictly to the following response format.
# Don't output anything else that outside the response format.

# Here is a sample of the response format.
# step-by-step think: your step by step think for rank the contexts
# idx: [index of the highest scoring context, index of the second highest scoring context, index of the third highest scoring context, index of the fourth highest scoring context, index of the fifth highest scoring context, index of the sixth highest scoring context, index of the seventh highest scoring context, index of the eighth highest scoring context]

# For example: 
# step-by-step think:"Arthur's Magazine" context: It directly relates to the claim as it mentions "Arthur's Magazine" and provides information about its publication period. It is informative and likely contains the answer to the claim. 2. "First for Women" context: This context directly mentions "First for Women," which is part of the claim. It provides information about the magazine, its publisher, and publication date. It is relevant and likely contains the answer to the claim. 3. "Radio City (Indian radio station)" context: Although it does not directly relate to the claim, it provides detailed information about a different topic. However, it might not be as relevant or likely to contain the answer compared to the contexts directly related to the claim. 4. "William Rast" context: This context provides information about a clothing line founded by Justin Timberlake and Trace Ayala. It is informative but not directly relevant to the claim about magazines. 5. "Women's colleges in the Southern United States" context: This context discusses women's colleges in the Southern United States, which is not directly related to the claim about magazines. It is informative but less likely to contain the answer compared to the contexts that directly mention the magazines in question.
# idx: [1,8,2,5,6,7,3,9]
'''

Supporting_prompt_V2_9th = '''
# You are a text Question-Answer agent, Now you are serving as a reranker. Given a claim to answer and a collection of potentially useful context about the claim.
# The format of each piece of context: {"idx":[context index], "title":[context title], "paragraph_text":[content of the context]}
# you should rank the given contexts according to the following rules:
# 1. The more relevant the context is to the claim, the higher the score is. 
# 2. The more likely the context may contain the answer to the claim, the higher the score is. 
# Please carefully consider the relevance, informativeness, and likelihood of containing the answer when ranking the contexts, and output the top 9 ranked contexts based on the scores..
# You should think step by step and rank the documents above carefully according to the rules.

# Here is a sample of the input format.
# Question: [The claim to be addressed]
# Context: [Collection of relevant contexts]
'''

Supporting_output_prompt_V2_9th = '''
# Please adhere strictly to the following response format.
# Don't output anything else that outside the response format.

# Here is a sample of the response format.
# step-by-step think: your step by step think for rank the contexts
# idx: [index of the highest scoring context, index of the second highest scoring context, index of the third highest scoring context, index of the fourth highest scoring context, index of the fifth highest scoring context, index of the sixth highest scoring context, index of the seventh highest scoring context, index of the eighth highest scoring context, index of the nineth highest scoring context]

# For example: 
# step-by-step think:"Arthur's Magazine" context: It directly relates to the claim as it mentions "Arthur's Magazine" and provides information about its publication period. It is informative and likely contains the answer to the claim. 2. "First for Women" context: This context directly mentions "First for Women," which is part of the claim. It provides information about the magazine, its publisher, and publication date. It is relevant and likely contains the answer to the claim. 3. "Radio City (Indian radio station)" context: Although it does not directly relate to the claim, it provides detailed information about a different topic. However, it might not be as relevant or likely to contain the answer compared to the contexts directly related to the claim. 4. "William Rast" context: This context provides information about a clothing line founded by Justin Timberlake and Trace Ayala. It is informative but not directly relevant to the claim about magazines. 5. "Women's colleges in the Southern United States" context: This context discusses women's colleges in the Southern United States, which is not directly related to the claim about magazines. It is informative but less likely to contain the answer compared to the contexts that directly mention the magazines in question.
# idx: [1,8,2,5,6,7,3,9,4]
'''

Supporting_prompt_V2_7th = '''
# You are a text Question-Answer agent, Now you are serving as a reranker. Given a claim to answer and a collection of potentially useful context about the claim.
# The format of each piece of context: {"idx":[context index], "title":[context title], "paragraph_text":[content of the context]}
# you should rank the given contexts according to the following rules:
# 1. The more relevant the context is to the claim, the higher the score is. 
# 2. The more likely the context may contain the answer to the claim, the higher the score is. 
# Please carefully consider the relevance, informativeness, and likelihood of containing the answer when ranking the contexts, and output the top 7 ranked contexts based on the scores..
# You should think step by step and rank the documents above carefully according to the rules.

# Here is a sample of the input format.
# Question: [The claim to be addressed]
# Context: [Collection of relevant contexts]
'''

Supporting_output_prompt_V2_7th = '''
# Please adhere strictly to the following response format.
# Don't output anything else that outside the response format.

# Here is a sample of the response format.
# step-by-step think: your step by step think for rank the contexts
# idx: [index of the highest scoring context, index of the second highest scoring context, index of the third highest scoring context, index of the fourth highest scoring context, index of the fifth highest scoring context, index of the sixth highest scoring context, index of the seventh highest scoring context]

# For example: 
# step-by-step think:"Arthur's Magazine" context: It directly relates to the claim as it mentions "Arthur's Magazine" and provides information about its publication period. It is informative and likely contains the answer to the claim. 2. "First for Women" context: This context directly mentions "First for Women," which is part of the claim. It provides information about the magazine, its publisher, and publication date. It is relevant and likely contains the answer to the claim. 3. "Radio City (Indian radio station)" context: Although it does not directly relate to the claim, it provides detailed information about a different topic. However, it might not be as relevant or likely to contain the answer compared to the contexts directly related to the claim. 4. "William Rast" context: This context provides information about a clothing line founded by Justin Timberlake and Trace Ayala. It is informative but not directly relevant to the claim about magazines. 5. "Women's colleges in the Southern United States" context: This context discusses women's colleges in the Southern United States, which is not directly related to the claim about magazines. It is informative but less likely to contain the answer compared to the contexts that directly mention the magazines in question.
# idx: [1,8,2,5,6,7,3]
'''

Supporting_prompt_V2_6th = '''
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

Supporting_output_prompt_V2_6th = '''
# Please adhere strictly to the following response format.
# Don't output anything else that outside the response format.

# Here is a sample of the response format.
# step-by-step think: your step by step think for rank the contexts
# idx: [index of the highest scoring context, index of the second highest scoring context, index of the third highest scoring context, index of the fourth highest scoring context, index of the fifth highest scoring context, index of the sixth highest scoring context]

# For example: 
# step-by-step think:"Arthur's Magazine" context: It directly relates to the claim as it mentions "Arthur's Magazine" and provides information about its publication period. It is informative and likely contains the answer to the claim. 2. "First for Women" context: This context directly mentions "First for Women," which is part of the claim. It provides information about the magazine, its publisher, and publication date. It is relevant and likely contains the answer to the claim. 3. "Radio City (Indian radio station)" context: Although it does not directly relate to the claim, it provides detailed information about a different topic. However, it might not be as relevant or likely to contain the answer compared to the contexts directly related to the claim. 4. "William Rast" context: This context provides information about a clothing line founded by Justin Timberlake and Trace Ayala. It is informative but not directly relevant to the claim about magazines. 5. "Women's colleges in the Southern United States" context: This context discusses women's colleges in the Southern United States, which is not directly related to the claim about magazines. It is informative but less likely to contain the answer compared to the contexts that directly mention the magazines in question.
# idx: [1,8,2,5,6,7]
'''

Supporting_prompt_V2_4th = '''
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

Supporting_output_prompt_V2_4th = '''
# Please adhere strictly to the following response format,
# Don't output anything else that outside the response format.

# Here is a sample of the output format.
# step-by-step think: your step by step think for rank the contexts
# idx: [index of the highest scoring context, index of the second highest scoring context, index of the third highest scoring context, index of the fourth highest scoring context]
# For example: 
# step-by-step think:1. "Arthur's Magazine" context: It directly relates to the claim as it mentions "Arthur's Magazine" and provides information about its publication period. It is informative and likely contains the answer to the claim. 2. "First for Women" context: This context directly mentions "First for Women," which is part of the claim. It provides information about the magazine, its publisher, and publication date. It is relevant and likely contains the answer to the claim. 3. "Radio City (Indian radio station)" context: Although it does not directly relate to the claim, it provides detailed information about a different topic. However, it might not be as relevant or likely to contain the answer compared to the contexts directly related to the claim. 4. "William Rast" context: This context provides information about a clothing line founded by Justin Timberlake and Trace Ayala. It is informative but not directly relevant to the claim about magazines. 5. "Women's colleges in the Southern United States" context: This context discusses women's colleges in the Southern United States, which is not directly related to the claim about magazines. It is informative but less likely to contain the answer compared to the contexts that directly mention the magazines in question.
# idx: [1,8,2,5]
'''

Supporting_prompt_V2_3th = '''
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

Supporting_output_prompt_V2_3th = '''
# Please adhere strictly to the following response format,
# Don't output anything else that outside the response format.

# Here is a sample of the output format.
# step-by-step think: your step by step think for rank the contexts
# idx: [index of the highest scoring context, index of the second highest scoring context, index of the third highest scoring context]
# For example: 
# step-by-step think:1. "Arthur's Magazine" context: It directly relates to the claim as it mentions "Arthur's Magazine" and provides information about its publication period. It is informative and likely contains the answer to the claim. 2. "First for Women" context: This context directly mentions "First for Women," which is part of the claim. It provides information about the magazine, its publisher, and publication date. It is relevant and likely contains the answer to the claim. 3. "Radio City (Indian radio station)" context: Although it does not directly relate to the claim, it provides detailed information about a different topic. However, it might not be as relevant or likely to contain the answer compared to the contexts directly related to the claim. 4. "William Rast" context: This context provides information about a clothing line founded by Justin Timberlake and Trace Ayala. It is informative but not directly relevant to the claim about magazines. 5. "Women's colleges in the Southern United States" context: This context discusses women's colleges in the Southern United States, which is not directly related to the claim about magazines. It is informative but less likely to contain the answer compared to the contexts that directly mention the magazines in question.
# idx: [1,8,2]
'''

Supporting_prompt_V2_2ed = '''
# You are a text Question-Answer agent, Now you are serving as a reranker. Given a claim to answer and a collection of potentially useful context about the claim.
# The format of each piece of context: {"idx":[context index], "title":[context title], "paragraph_text":[content of the context]}
# you should rank the given contexts according to the following rules:
# 1. The more relevant the context is to the claim, the higher the score is. 
# 2. The more likely the context may contain the answer to the claim, the higher the score is. 
# Please carefully consider the relevance, informativeness, and likelihood of containing the answer when ranking the contexts, and output the top 2 ranked contexts based on the scores..
# You should think step by step and rank the documents above carefully according to the rules.

# Here is a sample of the input format.
# Question: [The claim to be addressed]
# Context: [Collection of relevant contexts]
'''

Supporting_output_prompt_V2_2ed = '''
# Please adhere strictly to the following response format,
# Don't output anything else that outside the response format.

# Here is a sample of the output format.
# step-by-step think: your step by step think for rank the contexts
# idx: [index of the highest scoring context, index of the second highest scoring context]
# For example: 
# step-by-step think:1. "Arthur's Magazine" context: It directly relates to the claim as it mentions "Arthur's Magazine" and provides information about its publication period. It is informative and likely contains the answer to the claim. 2. "First for Women" context: This context directly mentions "First for Women," which is part of the claim. It provides information about the magazine, its publisher, and publication date. It is relevant and likely contains the answer to the claim. 3. "Radio City (Indian radio station)" context: Although it does not directly relate to the claim, it provides detailed information about a different topic. However, it might not be as relevant or likely to contain the answer compared to the contexts directly related to the claim. 4. "William Rast" context: This context provides information about a clothing line founded by Justin Timberlake and Trace Ayala. It is informative but not directly relevant to the claim about magazines. 5. "Women's colleges in the Southern United States" context: This context discusses women's colleges in the Southern United States, which is not directly related to the claim about magazines. It is informative but less likely to contain the answer compared to the contexts that directly mention the magazines in question.
# idx: [1,8]
'''

Supporting_prompt_V2_Ablation_2ed = '''
# You are a text Question-Answer agent, Now you are serving as a reranker. Given a claim to answer and a collection of potentially useful context about the claim.
# The format of each piece of context: {"idx":[context index], "title":[context title], "paragraph_text":[content of the context]}
# There are only 2 contexts are related to the claim.
# Output the 2 related contexts.

# Here is a sample of the input format.
# Question: [The claim to be addressed]
# Context: [Collection of relevant contexts]
'''

Supporting_output_prompt_V2_Ablation_2ed = '''
# Please adhere strictly to the following response format,
# Don't output anything else that outside the response format.

# Here is a sample of the output format.
# idx: [index of the first related context, index of the second related context]
# For example: 
# idx: [1,8]
'''