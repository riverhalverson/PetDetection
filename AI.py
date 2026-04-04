from datetime import datetime
import openai
from anthropic import Anthropic
import os
from openai import OpenAI
from Pets import Pet
import asyncio
from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer
from dotenv import load_dotenv
from pathlib import Path
import base64


class Prompts:
    # Get env variables
    load_dotenv()
    # Get API key from .env
    anthApiKey = os.getenv("ANTHROPIC_API_KEY")
    openaiApiKey = os.getenv("OPENAI_API_KEY")

    # Create clients
    anthClient = Anthropic(api_key=anthApiKey)
    openaiClient = OpenAI(api_key=openaiApiKey)

    def getPetSonaText(self, petName, imageLocation):
        pet = Pet()
        pet.setPet(petName)
        
        imageDescription = Prompts.getImageDescription(self, imageLocation)

        prompt = ("""
                  Give me a funny and extremely goofy short story about my pet, using what they're doing right now as context,
                  then tell us a story about how the pet got in this situation,
                  Make it extremely goofy and absolutely unhinged, to a ridiculous level.
                  """)
        prompt = Prompts.addImageDescription(self, prompt, imageDescription)
        prompt = Prompts.addPetTraits(self, prompt, pet)
        prompt = Prompts.addFormattingTraits(self, prompt)

        print(prompt)

        response = Prompts.anthClient.messages.create(max_tokens=1024, 
                                                    messages=[
                                                        {
                                                            "role": "user",
                                                            "content": prompt,
                                                        }
                                                    ],
                                                    model="claude-opus-4-6",
        )
        #result = Prompts.getPlainText(self,response)
        text = response.content[0].text

        Prompts.saveOutput(self, text)

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

        with Prompts.oepnaiClient.audio.speech.with_streaming_response.create(
                model = "gpt-4o-mini-tts",
                voice = "onyx",
                input = prompt,
                instructions = "Speak in an old timey war voice, sounding very very dramatic and cinematic",
        ) as response:
            response.stream_to_file(speechFile)

        return speechFile

    async def getPetSonaVoiceRT(self, petName, imageLocation):
        pet = Pet()
        pet.setPet(petName)

        prompt = Prompts.getPetSonaText(self, petName, imageLocation)


        openai = AsyncOpenAI()
        async with openai.audio.speech.with_streaming_response.create(
                model="gpt-4o-mini-tts",
                voice="onyx",
                input=prompt,
                instructions="Speak in a cheerful and positive tone.",
                response_format="pcm",
        ) as response:
            await LocalAudioPlayer().play(response)

    def getImageDescription(self, imageLocation):
        prompt = """Describe what the pet is doing in this image, do not mention the detection label or the box in your response,
                focus on the pet and do not get destracted by the things around the room, unless its right by the pet. do not guess
                the pets breed or type. But you can guess on things such as their mood and what they're doing, make what they're 
                doing right now as the basis of the story, it should be the focus.
                """

        with open(imageLocation, "rb") as image_file:
            imageData = base64.standard_b64encode(image_file.read()).decode("utf-8")

        imageDescription = Anthropic().messages.create(
            model="claude-opus-4-6",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": imageData,
                            },
                        },
                        {"type": "text", "text": prompt},
                    ],
                }
            ],
        )
        return imageDescription.content[0].text
    
    def addImageDescription(self, prompt, imageDescription):
        prompt += ("""Here is what you see, use the following as a reference to build your story and to give
                   relevant context: """ + imageDescription)
        
        return prompt

    def addFormattingTraits(self, prompt):
        prompt += ("""Format the text output while following these rules: 
                    dont use symbols or other formatting of any kind,
                    except new line terminating characters, text only. Add a newline before and after the finished 
                   prompt""")
        
        return prompt
        

    def addPetTraits(self, prompt, pet):
        prompt += ("Their name is: " + pet.name + ", they are a " + pet.gender + " " + pet.species + ". They like: " +
                  pet.likes + " and they dislike: " + pet.dislikes + ". You can use some of them but not all of them")

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
    
    def saveOutput(self, outputText):
        currentDateTime = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

        with open("output.txt", "a") as file:
            file.write("\n\n")
            file.write(currentDateTime)
            file.write(outputText)
            file.write("\n\n")
