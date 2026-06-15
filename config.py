import os
import json
from dotenv import load_dotenv

load_dotenv()

def get_llm_config():
    config_list = [
        {
            "model": os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            "api_key": os.getenv("AZURE_OPENAI_API_KEY"),
            "base_url": os.getenv("AZURE_OPENAI_ENDPOINT"),
            "api_type": "azure",
            "api_version": os.getenv("AZURE_OPENAI_API_VERSION")
        }
    ]

    with open("OAI_CONFIG_LIST.json", "w") as f:
        json.dump(config_list, f, indent=2)

    return {
        "config_list": config_list,
        "temperature": 0,
        "timeout": 120
    }

def get_docker_config():
    """
    Configure l'exécution du code généré par AutoGen
    dans le container Docker executor-sandbox
    """
    return {
        "use_docker": "executor-sandbox",  # nom de l'image Docker
        "timeout": 60,                      # max 60 secondes par exécution
        "work_dir": "sandbox"               # dossier de travail dans le container
    }

if __name__ == "__main__":
    config = get_llm_config()
    print("OAI_CONFIG_LIST.json créé avec succès !")
    print(f"Endpoint : {config['config_list'][0]['base_url']}")
    print(f"Modèle : {config['config_list'][0]['model']}")

    docker_config = get_docker_config()
    print("\n✅ Docker config :")
    print(f"Image utilisée : {docker_config['use_docker']}")
    print(f"Timeout : {docker_config['timeout']} secondes")
    print(f"Dossier : {docker_config['work_dir']}")