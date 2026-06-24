import autogen
from config import get_llm_config, get_docker_config
from agents.planner_agent import planner
from agents.executor_agent import executor
from agents.critic_agent import critic

llm_config = get_llm_config()
docker_config = get_docker_config()

user_proxy = autogen.UserProxyAgent(
    name="UserProxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    code_execution_config=docker_config,
    is_termination_msg=lambda msg: (
        "APPROVED" in msg.get("content", "") or
        "FALLBACK_HUMAIN" in msg.get("content", "")
    )
)

groupchat = autogen.GroupChat(
    agents=[user_proxy, planner, executor, critic],
    messages=[],
    max_round=20
)

manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

buggy_script = """
import pandas as pd
import numpy as np

def calculer_moyenne(valeurs):
    return sum(valeurs) / len(valeurs)

def afficher_stats(data):
    print("Moyenne :", moyenne)
    print("Max :", max(data))

valeur = []
valeurs = [10, 20, "30", 40, 50]
print("Résultat :", calculer_moyenne(valeur))
afficher_stats(valeurs)
"""

user_proxy.initiate_chat(
    manager,
    message=f"""Voici un script Python buggé à déboguer.

Le Planner décompose les étapes de débogage.
L'Executor exécute d'abord le script buggé tel quel, puis corrige les bugs.
Le Critic analyse les erreurs et valide les corrections.

Script buggé :
```python
{buggy_script}
```
"""
)