import autogen
from config import get_llm_config, get_docker_config

llm_config = get_llm_config()
docker_config = get_docker_config()

executor = autogen.AssistantAgent(
    name="Executor",
    system_message="""Tu es un agent exécuteur expert en Python.

Ton rôle est de recevoir un plan d'action et d'écrire du code Python pour l'accomplir.

Règles strictes :
1. Tu génères UNIQUEMENT du code Python syntaxiquement valide.
2. Chaque script doit être complet et exécutable.
3. Tu utilises uniquement ces bibliothèques : pandas, matplotlib, numpy, scipy, seaborn.
4. Tu mets toujours le code dans un bloc ```python ```.
5. Tu gères les erreurs avec try/except.
6. Tu affiches toujours les résultats avec print().""",
    llm_config=llm_config
)

user_proxy = autogen.UserProxyAgent(
    name="UserProxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=5,
    code_execution_config=docker_config
)