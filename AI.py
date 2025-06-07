from datetime import datetime
import openai
import os
from openai import OpenAI
from Pets import Pet
import asyncio
from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer
from dotenv import load_dotenv
from pathlib import Path


class Prompts:
    # Get env variables
    load_dotenv()
    # Get API key from .env
    api_key = os.getenv("OPENAI_API_KEY")

    # Create OpenAI client
    client = OpenAI(api_key=api_key)

    def getPetSonaText(self, petName):
        pet = Pet()
        pet.setPet(petName)

        prompt = ("Give me a funny and goofy biography about my pet, start with greeting them as if you're talking to them" +
                  ", make it short, no more than 60 words or so, dont use symbols or formatting of any kind," +
                  " except new line terminating characters, text only. Make it extremely goofy and absolutely unhinged. " +
                  "Generate this prompt with a temperature of 0.8 for maximum randomness and creativity")
        prompt = Prompts.addPetTraits(self, prompt, pet)

        response = Prompts.client.responses.create(model = "gpt-4.1", input = prompt)
        #result = Prompts.getPlainText(self,response)
        text = response.output_text

        Prompts.readPrompt(self, text)

        return str(text)

    def getPetSonaVoice(self, petName):
        pet = Pet()
        pet.setPet(petName)

        time = datetime.now().strftime("%H-%M-%S")
        currentDir = os.getcwd()
        folder = os.path.dirname(currentDir)
        fileName = f"{time}_speech.mp3"
        speechFile = os.path.join(folder, fileName)

        prompt = Prompts.getPetSonaText(self, petName)

        with Prompts.client.audio.speech.with_streaming_response.create(
                model = "gpt-4o-mini-tts",
                voice = "onyx",
                input = prompt,
                instructions = "Speak in an old timey war voice, sounding very very dramatic and cinematic",
        ) as response:
            response.stream_to_file(speechFile)

        return speechFile

    async def getPetSonaVoiceRT(self, petName):
        pet = Pet()
        pet.setPet(petName)

        prompt = Prompts.getPetSonaText(self, petName)

        openai = AsyncOpenAI()
        async with openai.audio.speech.with_streaming_response.create(
                model="gpt-4o-mini-tts",
                voice="onyx",
                input=prompt,
                instructions="Speak in a cheerful and positive tone.",
                response_format="pcm",
        ) as response:
            await LocalAudioPlayer().play(response)


    def addPetTraits(self, prompt, pet):
        prompt += ("Their name is: " + pet.name + ", they are a " + pet.gender + " " + pet.species + ". They like: " +
                  pet.likes + " and they dislike: " + pet.dislikes)

        return prompt


    def readPrompt(self, promptText):
        print(promptText)

    def getPlainText(self, modelResponse):
        startingIndex = modelResponse.find("text=")
        endingIndex = modelResponse.find("type=")

        # Remove response in front of text
        result = modelResponse[startingIndex + len("text="):].strip()

        # Remove response after the desired test
        result = result[:endingIndex]

        return result
