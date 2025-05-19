from utils.speech_to_text import real_time_speech_to_text
from utils.text_to_speech import real_time_text_to_speech
from utils.conversation import generate_response

def main():
    print("Conversational AI (real-time speech)")
    print("Press Ctrl+C to exit.")

    history = []

    try:
        while True:
            # Step 1: Speech to text
            user_input = real_time_speech_to_text()
            print(f"User: {user_input}")
            history.append(("User", user_input))

            # Step 2: Generate response with history
            response = generate_response(history, user_input)
            print(f"Assistant: {response}")
            history.append(("Assistant", response))

            # Step 3: Text to speech
            real_time_text_to_speech(response)

    except KeyboardInterrupt:
        print("\nExiting the conversation. Goodbye!")

if __name__ == "__main__":
    main()