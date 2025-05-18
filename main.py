from utils.speech_to_text import real_time_speech_to_text
from utils.text_to_speech import real_time_text_to_speech
from utils.conversation import generate_response

def main():
    print("Real-Time Speech Conversation System with LangChain")
    print("Speak into the microphone to start the conversation.")
    print("Press Ctrl+C to exit.")

    try:
        while True:
            # Step 1: Convert speech to text
            user_input = real_time_speech_to_text()
            print(f"User: {user_input}")

            # Step 2: Generate a response using LangChain
            response = generate_response(user_input)
            print(f"Assistant: {response}")

            # Step 3: Convert response to speech
            real_time_text_to_speech(response)

    except KeyboardInterrupt:
        print("\nExiting the conversation. Goodbye!")

if __name__ == "__main__":
    main()