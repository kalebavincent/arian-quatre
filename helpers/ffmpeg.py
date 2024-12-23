import asyncio
import os
import time
from configs import Config
from pyrogram.types import Message


async def MergeVideo(input_file: str, user_id: int, message: Message, format_: str):
    """
    Fusionne plusieurs vidéos listées dans un fichier texte en une seule vidéo.

    Args:
        input_file (str): Chemin vers le fichier texte contenant les vidéos à fusionner.
        user_id (int): ID de l'utilisateur pour identifier le fichier fusionné.
        message (Message): Message Pyrogram à mettre à jour avec la progression.
        format_ (str): Format de sortie de la vidéo (ex : mp4, mkv).

    Returns:
        str | None: Chemin du fichier fusionné ou None si une erreur survient.
    """
    output_vid = f"{Config.DOWN_PATH}/{str(user_id)}/[@hyoshdesign]_Merged.{format_.lower()}"
    file_generator_command = [
        "ffmpeg",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        input_file,
        "-c",
        "copy",
        output_vid
    ]
    
    try:
        process = await asyncio.create_subprocess_exec(
            *file_generator_command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
    except NotImplementedError:
        await message.edit(
            text=(
                "Impossible d'exécuter la commande FFmpeg ! Erreur : `NotImplementedError`.\n\n"
                "Veuillez exécuter ce bot dans un environnement Linux/Unix."
            )
        )
        await asyncio.sleep(10)
        return None

    await message.edit("Fusion des vidéos en cours...\n\nMerci de patienter...")
    stdout, stderr = await process.communicate()

    e_response = stderr.decode('latin-1', errors='ignore').strip()  
    t_response = stdout.decode('latin-1', errors='ignore').strip()

    print("Erreur FFmpeg:", e_response)
    print("Sortie FFmpeg:", t_response)

    return output_vid if os.path.lexists(output_vid) else None


async def cult_small_video(video_file: str, output_directory: str, start_time: str, end_time: str, format_: str):
    """
    Découpe une partie spécifique d'une vidéo.

    Args:
        video_file (str): Chemin de la vidéo source.
        output_directory (str): Répertoire où sauvegarder le fichier découpé.
        start_time (str): Heure de début (format HH:MM:SS ou en secondes).
        end_time (str): Heure de fin (format HH:MM:SS ou en secondes).
        format_ (str): Format de sortie (ex : mp4, mkv).

    Returns:
        str | None: Chemin du fichier découpé ou None si une erreur survient.
    """
    output_file = os.path.join(output_directory, f"{round(time.time())}.{format_.lower()}")
    file_generator_command = [
        "ffmpeg",
        "-i",
        video_file,
        "-ss",
        str(start_time),
        "-to",
        str(end_time),
        "-async",
        "1",
        "-strict",
        "-2",
        output_file
    ]

    process = await asyncio.create_subprocess_exec(
        *file_generator_command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()

    e_response = stderr.decode('latin-1', errors='ignore').strip() 
    t_response = stdout.decode('latin-1', errors='ignore').strip()

    print("Erreur FFmpeg:", e_response)
    print("Sortie FFmpeg:", t_response)

    return output_file if os.path.lexists(output_file) else None


async def generate_screen_shots(video_file: str, output_directory: str, no_of_photos: int, duration: int):
    """
    Génère des captures d'écran d'une vidéo à intervalles réguliers.

    Args:
        video_file (str): Chemin de la vidéo source.
        output_directory (str): Répertoire où sauvegarder les captures.
        no_of_photos (int): Nombre de captures à générer.
        duration (int): Durée totale de la vidéo en secondes.

    Returns:
        list[str]: Liste des chemins des captures générées.
    """
    images = []
    ttl_step = duration // no_of_photos
    current_ttl = ttl_step

    for _ in range(no_of_photos):
        await asyncio.sleep(1)  
        screenshot_path = os.path.join(output_directory, f"{str(time.time())}.jpg")
        file_generator_command = [
            "ffmpeg",
            "-ss",
            str(round(current_ttl)),
            "-i",
            video_file,
            "-vframes",
            "1",
            screenshot_path
        ]
        process = await asyncio.create_subprocess_exec(
            *file_generator_command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()

        e_response = stderr.decode('latin-1', errors='ignore').strip()  
        t_response = stdout.decode('latin-1', errors='ignore').strip()

        print("Erreur FFmpeg:", e_response)
        print("Sortie FFmpeg:", t_response)

        current_ttl += ttl_step
        images.append(screenshot_path)

    return images
