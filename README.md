### Anticipate & Act : Integrating LLMs and Classical Planning for Efficient Task Execution in Household Environments

This is the code release for the paper [Anticipate & Act](https://raraghavarora.github.io/ahsoka). It contains code for replicating the results of LLM based task anticipation and PDDL based action planning.

### :house: Household Domain
PDDL Domain for common household tasks like cooking, laundry can be found 
**[here](https://github.com/AnticipateAndAct/AnticipateAndAct/tree/main/PDDL)**. This domain consists of 33 actions, 5 different rooms, 33 objects distributed over 5-10 types, and 19 receptacles. We perform experiments on this domain using the [Fast Downward](https://www.fast-downward.org/) planner.

### :robot: Querying Large Language Models
The code for querying different LLMs: PaLM, GPT-3.5 and GPT-4 is **[here](LLM/)**. To run these files, replace the API keys at [LLM/keyconfig.py](LLM/keyconfig.py) with your PaLM and GPT API keys. For querying GPT models, we use [Azure OpenAI service](https://azure.microsoft.com/en-us/blog/introducing-gpt4-in-azure-openai-service/) and it can be set up using [these instructions](https://learn.microsoft.com/en-us/azure/ai-services/openai/quickstart?tabs=command-line&pivots=programming-language-python). Replace the `api_type`, `api_base` and `engine_name` at the starting lines of [LLM/azure_gpt.py](LLM/azure_gpt.py) with your service parameters.

**:rocket: More code coming soon..**
<!--
**AnticipateAndAct/AnticipateAndAct** is a ✨ _special_ ✨ repository because its `README.md` (this file) appears on your GitHub profile.

Here are some ideas to get you started:


- 🔭 I’m currently working on ...
- 🌱 I’m currently learning ...
- 👯 I’m looking to collaborate on ...
- 🤔 I’m looking for help with ...
- 💬 Ask me about ...
- 📫 How to reach me: ...
- 😄 Pronouns: ...
- ⚡ Fun fact: ...
-->
