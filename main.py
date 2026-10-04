import asyncio
import os

from dotenv import load_dotenv
from rodiumai import RodiumAI


load_dotenv()

API_KEY = os.getenv("RODIUMAI_API_KEY")


async def chat(client):
    question = input("\nVotre question : ")

    response = await client.chat(
        model="openai/gpt-4o",
        messages=[
            {
                "role": "user",
                "content": question,
            }
        ],
    )

    print("\nRéponse du modèle :")
    print(response.choices[0].message.content)

    print("\nCoût :", response.cost_rodi, "RODI")

    while True:
        choix = input(
            "\n[r] Refaire le chat  [s] Suivant : "
        ).lower()

        if choix == "r":
            return "repeat"

        if choix == "s":
            return "next"

        print("Choix invalide. Tapez r ou s.")


async def main():
    if not API_KEY:
        print("Erreur : RODIUMAI_API_KEY est absente.")
        print("Vérifiez votre fichier .env.")
        return

    client = RodiumAI(api_key=API_KEY)

    print("Client RodiumAI créé avec succès.")

    while True:
        action = await chat(client)

        if action == "repeat":
            continue

        if action == "next":
            break

    print("\nPassage à l'étape Image...")


if __name__ == "__main__":
    asyncio.run(main())