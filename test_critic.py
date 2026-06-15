import autogen
from config import get_llm_config

llm_config = get_llm_config()

critic = autogen.AssistantAgent(
    name="Critic",
    system_message="""Tu es un agent critique expert en Python.
Analyse le code et les résultats fournis.
Si tout est correct → réponds UNIQUEMENT par : 'APPROVED'
Si erreur → explique et propose une correction précise.
Tu ne génères jamais de nouveau code.""",
    llm_config=llm_config
)

user = autogen.UserProxyAgent(
    name="User",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=1,
    code_execution_config=False
)

# Test 1 — code correct
user.initiate_chat(
    critic,
    message="""Analyse ce code et son résultat :
Code :
numbers = [10, 20, 30, 40, 50]
moyenne = sum(numbers) / len(numbers)
print(f'Moyenne : {moyenne}')

Résultat : Moyenne : 30.0
Est-ce correct ?"""
)