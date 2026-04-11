import speech_recognition as sr
from dotenv import load_dotenv
load_dotenv()
from .graph import create_chat_graph 
from langgraph.checkpoint.mongodb import MongoDBSaver
import asyncio
from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer

openai = AsyncOpenAI()

MONGODB_URI = "mongodb://localhost:27017/"
config = {"configurable": {"thread_id": "voice_cursor_2"}}

def main():
    # Pass the custom DB name explicitly in the from_conn_string method!
    with MongoDBSaver.from_conn_string(MONGODB_URI, db_name="voice_cursor_db") as checkpointer:
        graph_with_mongo = create_chat_graph(checkpointer=checkpointer)
        
        
        # obtain audio from the microphone
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.pause_threshold = 3 # ya 3 seconds tak wait krega execute krna sa pahla agar silent hogya user speaking ka baad
            r.adjust_for_ambient_noise(source)  # listen for 1 second to calibrate the energy threshold for ambient noise levels

            while True:
                print("Say something!")
                audio = r.listen(source)

                # recognize speech using Google's Web Speech API
                try:
                    print("Processing audio...")
                    sst = r.recognize_google(audio)
                    print(f"You said: {sst}")
                    for event in graph_with_mongo.stream({ "messages": [{"role": "user", "content": sst}]}, config, stream_mode="values"):
                        if "messages" in event:
                            event["messages"][-1].pretty_print()

                except sr.UnknownValueError:
                    print("Could not understand audio")
                except sr.RequestError as e:
                    print(f"Could not request results from Google Speech Recognition service; {e}")


# tts : text to speech (not integrated now with project)
async def speak() -> None:
    async with openai.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="coral",
        input="Today is a wonderful day to build something people love!",
        instructions="Speak in a cheerful and positive tone.",
        response_format="pcm",
    ) as response:
        await LocalAudioPlayer().play(response)

# if __name__ == "__main__":
#     asyncio.run(speak())

main()