import autogen
from config import get_llm_config, get_docker_config

llm_config = get_llm_config()
docker_config = get_docker_config()

executor = autogen.AssistantAgent(
    name="Executor",
    system_message="""Tu es un agent exécuteur expert en Python.
Écris du code Python valide pour accomplir les tâches.
Utilise uniquement pandas, matplotlib, numpy.
Mets toujours le code dans un bloc ```python ```.
Affiche les résultats avec print().""",
    llm_config=llm_config
)

user_proxy = autogen.UserProxyAgent(
    name="UserProxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=3,
    code_execution_config=docker_config
)

user_proxy.initiate_chat(
    executor,
    message="Écris un script Python qui calcule la moyenne de [10, 20, 30, 40, 50] et affiche le résultat."
)