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
    max_consecutive_auto_reply=10, # max d'itérations
    code_execution_config=docker_config,
    is_termination_msg=lambda msg: "APPROVED" in msg.get("content", "") or "FALLBACK_HUMAIN" in msg.get("content", "")
)

groupchat = autogen.GroupChat(
    agents=[user_proxy, planner, executor, critic],
    messages=[],
    max_round=12 #limite des tours entre les agents
)

manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

user_proxy.initiate_chat(
    manager,
    message="Analyse le fichier ventes_data.csv : calcule le total des ventes, la moyenne par produit, et identifie le produit le plus vendu."
)