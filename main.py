import asyncio
import base64
import os

from dotenv import load_dotenv
from rodiumai import RodiumAI
from rodiumai.errors import InsufficientRODIError


load_dotenv()

API_KEY = os.getenv("RODIUMAI_API_KEY")


async def chat(client):
    question = input("\nVotre question : ")

    try:
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

    except InsufficientRODIError as error:
        print("\nSolde RODI insuffisant.")
        print(error)
        return "error"

    while True:
        choix = input(
            "\n[r] Refaire le chat  [s] Suivant : "
        ).lower()

        if choix == "r":
            return "repeat"

        if choix == "s":
            return "next"

        print("Choix invalide. Tapez r ou s.")


async def image(client):
    description = input("\nDescription de l'image : ")

    try:
        response = await client.images(
            model="openai/gpt-image-1.5",
            prompt=description,
            n=1,
            size="1024x1024",
        )

        image_base64 = response.data[0].b64_json
        image_bytes = base64.b64decode(image_base64)

        with open("image.png", "wb") as file:
            file.write(image_bytes)

        print("\nImage générée avec succès : image.png")

    except InsufficientRODIError as error:
        print("\nSolde RODI insuffisant.")
        print(error)
        return "error"

    while True:
        choix = input(
            "\n[b] Retour  [r] Refaire  [s] Suivant : "
        ).lower()

        if choix == "b":
            return "back"

        if choix == "r":
            return "repeat"

        if choix == "s":
            return "next"

        print("Choix invalide. Tapez b, r ou s.")


async def video(client):
    description = input("\nDescription de la vidéo : ")

    print("\nGénération de la vidéo en cours...")
    print("Cela peut prendre quelques instants...")

    try:
        response = await client.videos(
            model="openai/sora-2",
            prompt=description,
            duration_seconds=4,
            timeout=150,
        )

        video_data = response.data[0]

        if video_data.b64_json:
            video_bytes = base64.b64decode(video_data.b64_json)

            with open("video.mp4", "wb") as file:
                file.write(video_bytes)

            print("\nVidéo générée avec succès : video.mp4")

        elif video_data.url:
            print("\nVidéo générée avec succès.")
            print("URL :", video_data.url)

        else:
            print("\nAucune vidéo reçue.")

    except InsufficientRODIError as error:
        print("\nSolde RODI insuffisant.")
        print(error)
        return "error"

    return "next"


async def main():
    if not API_KEY:
        print("Erreur : RODIUMAI_API_KEY est absente.")
        print("Vérifiez votre fichier .env.")
        return

    client = RodiumAI(api_key=API_KEY)

    print("Client RodiumAI créé avec succès.")

    # Étape 1 : Chat
    while True:
        action = await chat(client)

        if action == "repeat":
            continue

        if action == "next":
            break

        if action == "error":
            return

    print("\nPassage à l'étape Image...")

    # Étape 2 : Image
    while True:
        action = await image(client)

        if action == "repeat":
            continue

        if action == "back":
            print("\nRetour au Chat...")
            return

        if action == "next":
            break

        if action == "error":
            return

    print("\nPassage à l'étape Vidéo...")

    # Étape 3 : Vidéo
    while True:
        action = await video(client)

        if action == "error":
            return

        if action == "next":
            break

    print("\nLes trois étapes sont terminées.")


if __name__ == "__main__":
    asyncio.run(main())