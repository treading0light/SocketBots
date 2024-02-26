from transformers import pipeline


if __name__ == "__main__":
    # Open the file and read the content
    with open("output.wav", "rb") as file:
        file_content = file.read()

    pipe = pipeline('automatic-speech-recognition', model="openai/whisper-small")
    print(pipe("output.wav"))