E2G_Base_prompt = '''
# You are a text Question-Answer agent. Given a context and a claim, please give a Answer to the claim based on the context.
# The format of the answer is {number or date or text}
#  Think step by step with evidence and explanation.
#  Generate both answer and step-by-step-reasoning-with-evidence-and-explanation 
# The format of your response is:   

# Here is a sample question-answer format:
# Question:What is the length of the track where the 2013 Liqui Moly Bathurst 12 Hour was staged?
# Answer: 6.213 km
# Evidence and explanation: The Mount Panorama Circuit, where the 2013 Liqui Moly Bathurst 12 Hour was staged, is 6.213 km long. This is stated in the context paragraph for the Mount Panorama Circuit.
# Step-by-step reasoning with evidence and explanation: Step 1: Identify the location of the 2013 Liqui Moly Bathurst 12 Hour - The context states that the event was staged at the Mount Panorama Circuit, near Bathurst, in New South Wales, Australia on 10 February 2013.Step 2: Find information about the Mount Panorama Circuit - The context paragraph for the Mount Panorama Circuit provides information about the track, including its length.Step 3: Locate the information about the length of the track - The context states that the track is 6.213 km long.Step 4: Confirm the answer - The length of the track is mentioned
'''

E2G_Gen_prompt = '''
# You are a text Question-Answer agent. Given a context and a claim, please give a Answer to the claim based on the context.
# The format of the answer is {number or date or text}
#  Think step by step with evidence and explanation.
#  Generate both answer and step-by-step-reasoning-with-evidence-and-explanation 
# The format of your response is: 
Answer: [Your answer]
Evidence and explanation:[Your Evidence and explanation]
Step-by-step reasoning with evidence and explanation: [Your Step-by-step reasoning with evidence and explanation]

# Here is a sample question-answer format:
# Question:What is the length of the track where the 2013 Liqui Moly Bathurst 12 Hour was staged?
# Answer: 6.213 km
# Evidence and explanation: The Mount Panorama Circuit, where the 2013 Liqui Moly Bathurst 12 Hour was staged, is 6.213 km long. This is stated in the context paragraph for the Mount Panorama Circuit.
# Step-by-step reasoning with evidence and explanation: Step 1: Identify the location of the 2013 Liqui Moly Bathurst 12 Hour - The context states that the event was staged at the Mount Panorama Circuit, near Bathurst, in New South Wales, Australia on 10 February 2013.Step 2: Find information about the Mount Panorama Circuit - The context paragraph for the Mount Panorama Circuit provides information about the track, including its length.Step 3: Locate the information about the length of the track - The context states that the track is 6.213 km long.Step 4: Confirm the answer - The length of the track is mentioned
'''

Test_prompt = '''
# 你是一个问题分析专家，现在给你一个需要回答的问题，以及问题相关的可能有效的信息的集合。
# 每一条信息的格式：{"idx":[信息的编号], "title":[信息的标题], "paragraph_text":[信息的内容]}
# 信息集合只有三条信息是对回答问题有效事实支持的信息，请你分析每一条信息的具体内容并将其与问题进行对比，找出三条有效事实支持的信息并输出。
#  根据你选出的信息回答给你的问题，请你使用证据和解释一步一步地思考。
#  同时生成答案以及一步一步思考用到的证据和解释。 

#输入格式：
问题：[输入的问题]
信息：[相关信息集合]

#  输入:
问题: What song recorded by Fergie was produced by Polow da Don and was followed by Life Goes On?
信息：{"idx": 0, "title": "M.I.L.F. $", "paragraph_text": "\"M.I.L.F. $\" (pronounced \"MILF money\") is a song recorded by American singer Fergie for her second studio album, \"Double Dutchess\" (2017). It was produced by Polow da Don and released as the second single from the record following \"L.A. Love (La La)\" on July 1, 2016 by Interscope and will.i.am Music Group. It debuted at number 34 on the US \"Billboard\" Hot 100 with 65,000 in first-week sales."}, 
{"idx": 1, "title": "London Bridge (Fergie song)", "paragraph_text": "\"London Bridge\" is a song recorded by American singer and rapper Fergie for her debut studio album, \"The Dutchess\" (2006). It was written by Fergie, Mike Hartnett, Sean Garrett, and producer Polow da Don. It was released as the lead single from the album and serviced to contemporary hit and rhythmic radio stations in the United States on July 18, 2006. \"London Bridge\" is a hip hop song with dance influences. It contains compositional samples of \"Down to The Nightclub\" as performed by Tower of Power."}, 
{"idx": 2, "title": "Cupid (Lloyd song)", "paragraph_text": "\"Cupid\" is the second single of Lloyd's fourth studio album \"King of Hearts\". It was released March 22, 2011 & it features Polow da Don under the name Awesome Jones!!!!. The track was produced by Polow da Don, Greg Curtis and written by Bei Maejor, Polow A. Jones, Jason Perry, Curtis. The horns were played by Siraaj Amnesia James. The single was only released in the United States, where it only reached #2 on the Bubbling Under Hot 100 chart."}, 
{"idx": 3, "title": "Promise (Ciara song)", "paragraph_text": "\"Promise\" is a song performed by American recording artist Ciara from her second studio album, \"\" (2006). It was written by Ciara, Jasper Cameron, Polow da Don and Elvis Williams and produced by Polow da Don. The remix features singer R. Kelly. The song was released as the album's official lead single on October 16, 2006, through LaFace Records. The song was selected as the first single as Ciara wanted to put out a single with a slower pace, noting that her previous releases had been up-tempo. According to Ciara, the song represents the album's theme of evolving and symbolizes her growth as a songwriter and artist."}, 
{"idx": 4, "title": "As Your Friend", "paragraph_text": "\"As Your Friend\" is a song by Dutch DJ Afrojack, featuring vocals by American singer Chris Brown. The song was released as a single via iTunes on 13 February 2013. It was written by Afrojack, Chris Brown, Nadir Sakir, Leroy Styles, DJ Buddha, and Polow Da Don, and was produced by Afrojack with co-production by Leroy Styles, DJ Buddha and Polow da Don. \"As Your Friend\" is featured as a bonus track on the deluxe version of Afrojack's 2014 debut studio album \"Forget the World\"."}, 
{"idx": 5, "title": "Life Goes On (Little Texas song)", "paragraph_text": "\"Life Goes On\" is a song recorded by American country music group Little Texas. It was released in August 1995 as the first single from the band's \"Greatest Hits\" album. The song was co-written by the band's drummer, Del Gray and songwriters Thom McHugh and Keith Folles\u00e9. \"Life Goes On\" was Little Texas's thirteenth entry on the \"Billboard\" charts, peaking at #5 on the Hot Country Songs chart and reaching #4 on Canada's \"RPM\" country tracks chart. It would be their last single to make it to the Top 40."}, 
{"idx": 6, "title": "Sweet Love (Chris Brown song)", "paragraph_text": "\"Sweet Love\" is a song by American recording artist Chris Brown, taken from his fifth studio album, \"Fortune\" (2012). It was written by Brown, Cory Marks, Greg Curtis, Jamal \"Polow da Don\" Jones, Jason \"JP\" Perry and Tommy Doyle Jr., while the production was handled by Polow da Don and Perry. The song was sent to urban contemporary radio in the United States on April 10, 2012, as the second single from the album. \"Sweet Love\" is a slow jam R&B ballad which incorporates elements of electronic music."}, 
{"idx": 7, "title": "Make Love", "paragraph_text": "\"Make Love\" is a song performed by American recording artist and songwriter Keri Hilson. It was written by Jamal \"Polow da Don\" Jones, Ester Dean and Jason Perry, and produced by Polow da Don and Perry for Hilson's debut studio album, \"In a Perfect World...\" (2009). The song was sent for urban adult contemporary airplay on June\u00a023, 2009 as the fifth single from the album. Musically, \"Make Love\" is a downtempo R&B ballad. The song received mixed reviews from music critics; some of them criticized its long length and Hilson's vocals, while others named it one of the album's standouts."}, 
{"idx": 8, "title": "Woohoo (Christina Aguilera song)", "paragraph_text": "\"Woohoo\" is a song by American singer Christina Aguilera, featuring Trinidadian rapper Nicki Minaj. The song was written by Aguilera, Onika Maraj, Claude Kelly, Ester Dean and Jamal \"Polow da Don\" Jones, and produced by Polow da Don, for Aguilera's sixth studio album, \"Bionic\" (2010). \"Woohoo\" was serviced to rhythmic contemporary crossover airplay as the album's second radio single on May 25, 2010. The song, which contains a sample of the 1972 song \"Add m\u00e1r uram az es\u0151t\" by Kati Kov\u00e1cs, is about oral sex."}, 
{"idx": 9, "title": "Life Goes On (Fergie song)", "paragraph_text": "\"Life Goes On\" is a song recorded by American singer Fergie for her second studio album, \"Double Dutchess\" (2017). It was released as single on November 11, 2016, by Interscope and will.i.am Music Group. The song serves as the third single from Fergie's second studio album, following \"M.I.L.F. $\". \"Life Goes On\" was written by Fergie, Tristan Prettyman, Keith Harris and Toby Gad."}

# 输出格式：
有效的信息1：{"idx":[你认为有效信息的编号],"title":[你认为有效信息的标题], "paragraph_text":[你认为有效信息的内容]}
有效的信息2：{"idx":[你认为有效信息的编号],"title":[你认为有效信息的标题], "paragraph_text":[你认为有效信息的内容]}
有效的信息3：{"idx":[你认为有效信息的编号],"title":[你认为有效信息的标题], "paragraph_text":[你认为有效信息的内容]}
答案: [你的答案]
证据和解释:[你的证据和解释]
带有证据和解释的一步一步思考: [你的带有证据和解释的一步一步思考]
'''

Supporting_prompt = '''
# You are a text Question-Answer agent. Given a claim to answer and a collection of potentially useful context about the claim.
# The format of each piece of context: {"idx":[context index], "title":[context title], "paragraph_text":[content of the context]}
# Please note that although the collection contains multiple pieces of contexts, only two are genuine and effective factual support contexts. 
# Your task is to meticulously sift through and analyze these pieces of contexts, identify the two that truly provide effective support for the answer to the claim.

# Here is a sample of the input format.
# Question: [The claim to be addressed]
# Context: [Collection of relevant contexts]
'''

Supporting_output_prompt = '''
# Here is a sample of the output format.
# idx: [Index of the first piece of information you deem effective, Index of the second piece of information you deem effective]
# For example: idx: [5,8]
'''

Evidence_prompt_v2 = '''
# You are a text Question-Answer agent. Given a claim to answer and a collection of potentially useful context about the claim.
# The format of each piece of context: {"idx":[context index], "title":[context title], "paragraph_text":[content of the context]}
# Please note that although the collection contains multiple pieces of contexts, only two are genuine and effective factual support contexts. 
# Your task is to meticulously sift through and analyze these pieces of contexts, identify the two that truly provide effective support for the answer to the claim.
# Based on the factual support contexts you have identified, please answer the claim.
# Think step by step with evidence and explanation.
# Generate both answer and step-by-step-reasoning-with-evidence-and-explanation 

# Here is a sample of the input format.
# Question: [The claim to be addressed]
# Context: [Collection of relevant contexts]
'''

Evidence_output_prompt_v2 = '''
# Please adhere strictly to the following response format.
# Your answer should be brief and directly follow "Answer:".
# Acceptable responses include Nouns, Dates, or a simple "yes" or "no".
# Avoid including lengthy narrative statements in the "Answer".

# The format of your response is:   
# Answer: [Answer]
# idx: [Index of the first piece of information you deem effective, Index of the second piece of information you deem effective]
# Evidence and explanation: [Evidence and explanation used in your think.]
# Step by step with evidence and explanation: [Step by step with evidence and explanation].

# Here is a sample output format:
# Answer: Musician and satirist Allie Goertz wrote a song about the "The Simpsons" character Milhouse, who Matt Groening named after who?
# idx: [5,8]
# Evidence and explanation: - The context with idx 8 states that Matt Groening, the creator of "The Simpsons," named the character Milhouse after President Richard Nixon's middle name. This directly provides the origin of the character's name. - The context with idx 0 provides additional information about Matt Groening, stating that he named the character Homer Simpson after his own father, Homer Groening. This establishes a pattern of Groening naming characters after real-life figures, supporting the idea that he named Milhouse after President Richard Nixon's middle name.
# Step by step with evidence and explanation: 1. The context with idx 8 directly states that Matt Groening named the character Milhouse after President Richard Nixon's middle name. This is a clear and explicit piece of information. 2. To further support this, we look at the context with idx 0, which shows that Matt Groening named the character Homer Simpson after his own father, Homer Groening. This establishes a pattern of Groening drawing inspiration from real-life names for his characters, making it plausible that he named Milhouse after President Nixon.
'''

Supporting_prompt_pro = '''
# You are a text Question-Answer agent. Given a claim to answer and a collection of potentially useful context about the claim.
# The format of each piece of context: {"idx":[context index], "title":[context title], "paragraph_text":[content of the context]}
# Please note that although the collection contains multiple pieces of contexts, only two are genuine and effective factual support contexts. 
# Think step by step with evidence and explanation.
# Your task is to meticulously sift through and analyze these pieces of contexts, identify the two that truly provide effective support for the answer to the claim.
# Generate both the indexes of context you identified and step-by-step-reasoning-with-evidence-and-explanation. 

# Here is a sample of the input format.
# Question: [The claim to be addressed]
# Context: [Collection of relevant contexts]
'''

Supporting_output_prompt_pro = '''
# Here is a sample of the output format.
# idx: [Index of the first piece of information you deem effective, Index of the second piece of information you deem effective]
# Step by step with evidence and explanation: [Step by step with evidence and explanation].

# Here is a sample output format: 
# idx: [3, 5]
# Step by step with evidence and explanation: First, the context at index 5 provides effective support for the claim. It states that Badr Hari was once considered the best kickboxer in the world, but has been involved in controversies relating to his "unsportsmanlike conducts" in the sport and crimes of violence outside of the ring. This directly addresses the claim about Badr Hari's status as a kickboxer and his involvement in controversies. Secondly, the context at index 0 also provides effective support for the claim. It mentions a Steel Cage Match that highlighted a feud involving Kick Boxer, which indicates his involvement in the sport. This supports the claim that Kick Boxer was once considered the best kickboxer in the world. Therefore, the contexts at index 5 and 0 are the most effective in providing support for the claim.
'''

Supporting_prompt_Sec = '''
# You are a text Question-Answer agent. Given a claim to answer and a collection of potentially useful context about the claim.
# The format of each piece of context: {"idx":[context index], "title":[context title], "paragraph_text":[content of the context]}
# Please note that although the collection contains multiple pieces of contexts, only three are genuine and effective factual support contexts. 
# Your task is to meticulously sift through and analyze these pieces of contexts, identify the Three that truly provide effective support for the answer to the claim.

# Here is a sample of the input format.
# Question: [The claim to be addressed]
# Context: [Collection of relevant contexts]
'''

Supporting_output_prompt_Sec = '''
# Here is a sample of the output format.
# idx: [Index of the first piece of information you deem effective, Index of the second piece of information you deem effective, Index of the third piece of information you deem effective]
# For example: idx: [2,5,8]
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

Supporting_prompt_Neg = '''
# You are a text Question-Answer agent. Given a claim to answer and a collection of potentially useful context about the claim.
# The format of each piece of context: {"idx":[context index], "title":[context title], "paragraph_text":[content of the context]}
# Please note that although the collection contains multiple pieces of contexts, but two are contexts with invalid information.
# Your task is to meticulously sift through and analyze these pieces of contexts
# You should think step by step and identify the two that provide most invalid information for the answer to the claim.

# Here is a sample of the input format.
# Question: [The claim to be addressed]
# Context: [Collection of Invalid contexts]
'''

Supporting_output_prompt_Neg = '''
# Please adhere strictly to the following response format,
# Don't output anything else that outside the response format.

# Here is a sample of the output format.
# step-by-step think: your step by step think for rank the contexts
# idx: [index of the first context with most invalid information, index of the second invalid context with second invalid information]
# For example:  step-by-step think:1. The Oberoi family is known for its involvement in the hotel industry, specifically through The Oberoi Group. 2. The Oberoi Group has its head office in Delhi, as mentioned in context 1. 3. Context 1 provides accurate information about the headquarters of The Oberoi Group. 4. Context 2 talks about a fiber optic sensing technologies company, not related to the hotel industry. 5. Context 3 discusses a historic hotel in Hartford, Connecticut, which is also not related to the headquarters of The Oberoi Group. 6. Context 4 is about a historic hotel in Glennville, Georgia, which is irrelevant to the claim. 7. Context 5 relates to the military police company and is unrelated to the Oberoi family or The Oberoi Group. 8. Context 6 pertains to the Tallcorn Towers Apartments in Iowa, not providing information about the Oberoi family's hotel business. 9. Context 7 discusses the Ritz-Carlton Jakarta in Indonesia, not relevant to the claim. 10. Context 8 mentions the Oberoi family and its involvement in hotels, aligning with the claim. 11. Context 9 focuses on Mohan Singh Oberoi, the founder of Oberoi Hotels & Resorts.
# idx: [2,4]
'''

'''# 2. The more informative the context is, the higher the score is. '''


Evidence_prompt_golden_pool = '''
# You are a text Question-Answer agent. Given a claim to answer and a collection of potentially useful context about the claim.
# The format of each piece of context: {"idx":[context index], "title":[context title], "paragraph_text":[content of the context], "is_supporting": true}
# Your task is to analyze these pieces of contexts, and answer the claim based on these contexts.
# Think step by step with evidence and explanation.
# Generate both answer and step-by-step-reasoning-with-evidence-and-explanation 

# Here is a sample of the input format.
# Question: [The claim to be addressed]
# Context: [Collection of relevant contexts]
'''

Evidence_output_prompt_golden_pool = '''
# Please adhere strictly to the following response format.
# Additionally, provide 2 high-quality potential candidate answers.
# Your potential answers should be brief and avoid including narrative statements. The answer must only contain the necessary nouns, phrases, or simple yes or no to answer the question.
# Score the 2 candidate answers based on:
#   1、The correctness of the answer (more accurate answers score higher)
#   2、The amount of useful information in the answer (more useful information scores higher)
#   3、The less of unnecessary statements in the answer (fewer unnecessary narrative statements scores higher)
# Select the highest-scoring answer as Answer:.
# And then you should write your Evidence and explanation and Step by step with evidence and explanation to show how you come out the answer.

# The format of your response is:   
# Candidate answers:[Candidate Answer 1,Candidate Answer 2]
# Answer: [Highest scoring answer]
# Evidence and explanation: [Evidence and explanation used in your think.]
# Step by step with evidence and explanation: [Step by step with evidence and explanation].

For example:
Example1:
Question: Were Scott Derrickson and Ed Wood of the same nationality?
Context:{'idx': 1, 'title': 'Scott Derrickson', 'paragraph_text': 'Scott Derrickson (born July 16, 1966) is an American director, screenwriter and producer. He lives in Los Angeles, California. He is best known for directing horror films such as "Sinister", "The Exorcism of Emily Rose", and "Deliver Us From Evil", as well as the 2016 Marvel Cinematic Universe installment, "Doctor Strange."'}, {'idx': 8, 'title': 'Ed Wood', 'paragraph_text': 'Edward Davis Wood Jr. (October 10, 1924 – December 10, 1978) was an American filmmaker, actor, writer, producer, and director.'}, {'idx': 2, 'title': 'Ed Wood (film)', 'paragraph_text': "Ed Wood is a 1994 American biographical period comedy-drama film directed and produced by Tim Burton, and starring Johnny Depp as cult filmmaker Ed Wood. The film concerns the period in Wood's life when he made his best-known films as well as his relationship with actor Bela Lugosi, played by Martin Landau. Sarah Jessica Parker, Patricia Arquette, Jeffrey Jones, Lisa Marie, and Bill Murray are among the supporting cast."}
Candidate answers: [Yes, No]
Answer: Yes
Evidence and explanation: Both Scott Derrickson and Ed Wood are described as American in the provided contexts.
Step by step with evidence and explanation:
1. The claim asks if Scott Derrickson and Ed Wood were of the same nationality.
2. Context index 1 states that Scott Derrickson is an American director.
3. Context index 8 describes Ed Wood as an American filmmaker.
4. Since both individuals are identified as American, the answer to the claim is yes, they were of the same nationality.

Example2:
Question:The director of the romantic comedy "Big Stone Gap" is based in what New York city?
Context:{'idx': 7, 'title': 'Adriana Trigiani', 'paragraph_text': 'Adriana Trigiani is an Italian American best-selling author of sixteen books, television writer, film director, and entrepreneur based in Greenwich Village, New York City. Trigiani has published a novel a year since 2000.'}, {'idx': 8, 'title': 'Big Stone Gap (film)', 'paragraph_text': "Big Stone Gap is a 2014 American drama romantic comedy film written and directed by Adriana Trigiani and produced by Donna Gigliotti for Altar Identity Studios, a subsidiary of Media Society. Based on Trigiani's 2000 best-selling novel of the same name, the story is set in the actual Virginia town of Big Stone Gap circa 1970s. The film had its world premiere at the Virginia Film Festival on November 6, 2014."}, {'idx': 3, 'title': 'Just Another Romantic Wrestling Comedy', 'paragraph_text': 'Just Another Romantic Wrestling Comedy is a 2006 film starring April Hunter and Joanie Laurer. This Romantic comedy film was premiered at New Jersey and New York City on December 1, 2006 and was released on DVD in the United States and the United Kingdom on April 17, 2007. After the film\'s DVD release "Just Another Romantic Wrestling Comedy" won an "Honorable Mention" award at the New Jersey International Festival awards. The release is being handled by "Victory Multimedia".'}
Candidate answers: [Greenwich Village, New York City, Greenwich Village]
Answer: Greenwich Village, New York City
Evidence and explanation: The director of "Big Stone Gap," Adriana Trigiani, is based in Greenwich Village, New York City, according to the context provided.
Step by step with evidence and explanation:
1. The question asks for the New York city where the director of the romantic comedy "Big Stone Gap" is based.
2. Context index 7 states that Adriana Trigiani, the director of "Big Stone Gap," is based in Greenwich Village, New York City.
3. The other contexts provided do not offer additional information about the location of Adriana Trigiani's base.
4. Therefore, the answer is that the director of "Big Stone Gap" is based in Greenwich Village, New York City. This answer is correct, relevant, and contains the most useful information among the candidate answers.
'''

'''
#   1、The amount of useful information in the answer (more useful information scores higher)
#   2、The less of unnecessary statements in the answer (fewer unnecessary narrative statements scores higher)
#   3、The relevance to the question (more relevant answers score higher)
#   4、The correctness of the answer (more accurate answers score higher)
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

Evidence_Reflexion_prompt_golden = '''
# Task:
# You are a text Question-Answer agent. Given a claim to answer and a collection of potentially useful context about the claim.
# The format of each piece of context: {"idx":[context index], "paragraph_text":[content of the context]}
# Answer can be found directly in the contexts., Your task is to analyze these pieces of contexts, and find the answer to this claim directly in these Contexts.
# You have attempted to answer this claim before and failed. The following reflections give a plan to avoid failing to answer the claim in the same way you did previously. Use them to improve your strategy of correctly answering the given claim.
# Reasoning:
# Think step by step with evidence and explanation.
# Generate both answer and step-by-step-reasoning-with-evidence-and-explanation 

# Here is a sample of the input format.
# Question: [The claim to be addressed]
# Context: [Collection of relevant contexts]
# Reflexion: [The Plan based on reflection]
'''

Evidence_Reflexion_output_prompt_golden = '''
# Please adhere strictly to the following response format.
# The format of your response is:   
# Answer: [Your Answer]
# Evidence and explanation: [Evidence and explanation used in your think.]
# Step by step with evidence and explanation: [Step by step with evidence and explanation].

# Note that Your response can only contain Answer, Evidence and explanation, and Step by step with evidence and explanation!
# In Answer:The answers can be simple [words], [phrases].  You must find the answers directly in these contexts. 
# Your answer should be brief and avoid including narrative statements.
# And then you should write your Evidence and explanation and Step by step with evidence and explanation to show how you come out the answer.
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