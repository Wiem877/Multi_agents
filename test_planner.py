import autogen
from config import get_llm_config

llm_config = get_llm_config()

planner = autogen.AssistantAgent(
    name="Planner",
    system_message="""Tu es un agent planificateur expert.
Décompose toute requête en étapes numérotées claires.
Tu ne génères JAMAIS de code, uniquement des instructions en langage naturel.
Termine toujours par 'Plan terminé.'""",
    llm_config=llm_config
)

user = autogen.UserProxyAgent(
    name="User",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=1, # répond une seule fois puis s'arrête
    code_execution_config=False
)

user.initiate_chat(
    planner,
    message="Analyse un fichier CSV contenant des ventes et génère un rapport statistique."
)