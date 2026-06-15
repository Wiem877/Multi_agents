import autogen
from config import get_llm_config

def test_connection():
    print("Connexion à Azure OpenAI en cours...")

    llm_config = get_llm_config()

    assistant = autogen.AssistantAgent(
        name="assistant",
        llm_config=llm_config,
        system_message="Tu es un assistant utile."
    )

    user = autogen.UserProxyAgent(
        name="user",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=1,
        code_execution_config=False
    )

    user.initiate_chat(
        assistant,
        message="Réponds uniquement par 'Connexion Azure OpenAI OK' pour valider le test."
    )

if __name__ == "__main__":
    test_connection()