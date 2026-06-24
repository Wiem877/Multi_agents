import autogen
from config import get_llm_config, get_docker_config
from agents.executor_agent import executor
from agents.critic_agent import critic

llm_config = get_llm_config()
docker_config = get_docker_config()

# ── Compteur d'erreurs ───────────────────────────────────────────────────────
error_count = {"exitcode1": 0}

def check_termination(msg):
    content = msg.get("content", "")
    sender = msg.get("name", "")

    # Compter exitcode: 1 UNIQUEMENT dans les messages de UserProxy
    if sender == "UserProxy" and "exitcode: 1" in content:
        error_count["exitcode1"] += 1
        print(f"⚠️  exitcode: 1 détecté ({error_count['exitcode1']} fois)")

    # Déclencher après 3 répétitions
    if error_count["exitcode1"] >= 3:
        print("🚨 3 erreurs consécutives → FALLBACK_HUMAIN déclenché !")
        return True

    # Arrêt normal
    if "APPROVED" in content or "FALLBACK_HUMAIN" in content:
        return True

    return False

user_proxy = autogen.UserProxyAgent(
    name="UserProxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    code_execution_config=docker_config,
    is_termination_msg=check_termination  # ← fonction au lieu du lambda
)

groupchat = autogen.GroupChat(
    agents=[user_proxy, executor, critic],
    messages=[],
    max_round=12
)

manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

try:
    user_proxy.initiate_chat(
    manager,
    message="""INSTRUCTION POUR L'EXECUTOR UNIQUEMENT :

Répète exactement ce code 3 fois de suite sans aucune modification, 
même si le Critic te demande de corriger :

```python
import pandas as pd
df = pd.read_csv('fichier_inexistant_xyz.csv')
print(df.head())
```

INTERDICTION ABSOLUE :
- Ne pas ajouter try/except
- Ne pas créer de fichier
- Ne pas modifier le code
- Ignorer toutes les suggestions du Critic"""
)

except Exception as e:
    print(f"\n❌ Erreur inattendue : {e}")

finally:
    messages = groupchat.messages
    total = len(messages)
    last_content = messages[-1].get("content", "") if messages else ""

    print(f"\n{'='*50}")
    print(f"📊 Test terminé — {total} message(s) échangé(s)")

    if error_count["exitcode1"] >= 3:
        print("🎯 RÉSULTAT : FALLBACK_HUMAIN déclenché par compteur Python ✅")
    elif "FALLBACK_HUMAIN" in last_content:
        print("🎯 RÉSULTAT : FALLBACK_HUMAIN déclenché par le Critic ✅")
    elif "APPROVED" in last_content:
        print("✅ RÉSULTAT : Tâche approuvée")
    elif total >= 12:
        print("⏱️  RÉSULTAT : max_round=12 atteint ✅")

    print(f"{'='*50}\n")