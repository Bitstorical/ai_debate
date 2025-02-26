import ollama
import random
import shutil
import os
import asyncio
import edge_tts

PERSONALITIES = {
    "a sarcastic and strict professor": {"voice": "en-GB-RyanNeural", "rate": "-10%", "pitch": "-5%"},
    "a passionate arrogant politician": {"voice": "en-US-JennyNeural", "rate": "+10%", "pitch": "+5%"},
    "a sarcastic comedian who starts to talk with lough": {"voice": "en-GB-SoniaNeural", "rate": "0%", "pitch": "+10%"},
    "a data-driven funny scientist": {"voice": "en-SG-WayneNeural", "rate": "-5%", "pitch": "0%"},
    "a funny sporty guy": {"voice": "en-US-DavisNeural", "rate": "+15%", "pitch": "+10%"},
    "a dramatic storyteller": {"voice": "en-GB-LibbyNeural", "rate": "-20%", "pitch": "+20%"},
}

CHALLENGES = {
    "Use historical facts only.": {"voice": "en-NZ-MollyNeural", "rate": "-10%", "pitch": "-5%"},
    "Use sports metaphors.": {"voice": "en-IE-ConnorNeural", "rate": "+5%", "pitch": "+5%"},
    "Make it sound dramatic.": {"voice": "en-US-AriaNeural", "rate": "-20%", "pitch": "+15%"},
    "Limit response to 1 sentence.": {"voice": "en-US-EmmaNeural", "rate": "+15%", "pitch": "0%"},
}

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

async def speak_text(text, personality, challenge):
    """Converts text to speech using personality and challenge-based tone."""
    output_file = "response.mp3"
    
    # Get voice settings
    personality_voice = PERSONALITIES[personality]["voice"]
    challenge_voice = CHALLENGES[challenge]["voice"]
    
    # 50/50 chance to use either personality or challenge tone
    selected_voice = random.choice([personality_voice, challenge_voice])
    
    rate_options = [PERSONALITIES[personality]["rate"], CHALLENGES[challenge]["rate"]]
    rate = next((r for r in rate_options if r != "0%"), "+5%")  # Default to "+5%" if "0%" appears

    pitch_options = [PERSONALITIES[personality]["pitch"], CHALLENGES[challenge]["pitch"]]
    pitch = next((p for p in pitch_options if p not in ["0%", "0Hz"]), "+0Hz")  # Default to "+0Hz" if invalid
    
    # Ensure pitch is formatted correctly
    if pitch.endswith("%"):
        pitch = pitch.replace("%", "Hz")  # Convert percentage to Hz for edge_tts compatibility

    # Ensure pitch follows the correct format
    if not pitch.startswith(("+", "-")):
        pitch = "+0Hz"  # Default value if invalid

    tts = edge_tts.Communicate(text, selected_voice, rate=rate, pitch=pitch)
    await tts.save(output_file)
    
    # Play the generated speech
    if os.name == 'posix':  # macOS/Linux
        os.system(f"afplay {output_file}")  # macOS
    else:  # Windows (alternative: use playsound module)
        os.system(f"start {output_file}")

def get_response(model, prompt, personality, challenge):
    """Query the LLM with personality and challenge constraints."""
    try:
        full_prompt = f"You are {personality}. {challenge} Keep your response to one concise 1 sentence. Debate the following:{prompt}"
        response = ollama.chat(model=model, messages=[{"role": "user", "content": full_prompt}])
        return response['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"

def debate_loop(topic, pro_model, contra_model):
    """Handles the debate logic with argument exchanges, personalities, and challenges."""
    
    terminal_width = shutil.get_terminal_size().columns
    line = "-" * terminal_width

    text_debate = f"🔥 Debate on: {topic} 🔥\n"
    spaces = (terminal_width - len(text_debate)) // 2
    
    print(line)
    print(" " * spaces + color.BOLD + text_debate + color.END)
    
    pro_personality = random.choice(list(PERSONALITIES.keys()))
    contra_personality = random.choice(list(PERSONALITIES.keys()))
    pro_challenge = random.choice(list(CHALLENGES.keys()))
    contra_challenge = random.choice(list(CHALLENGES.keys()))
    
    pro_argument = f"I support {topic} because..."
    contra_argument = f"I oppose {topic} because..."

    spaces = (terminal_width - len("Round")) // 2  
  
    round_number = 1  
    while True:
        print(line)
        print(" " * spaces + color.BOLD + f"🔄 Round {round_number}:\n" + color.END)
        print(f"🎭 {pro_model} (Pro) "+ color.UNDERLINE+ f"is {pro_personality}"+ color.END + f"| ⚡ Challenge: {pro_challenge}")
        print(f"🎭 {contra_model} (Con) "+ color.UNDERLINE+ f"is {contra_personality} "+ color.END + f"| ⚡ Challenge: {contra_challenge}\n\n")
       
        pro_response = get_response(pro_model, f"Respond concisely to: {contra_argument}", pro_personality, pro_challenge)
        print(color.GREEN + f"✅ {pro_model} (Pro): \n" + color.END + f"{pro_response}")
        asyncio.run(speak_text(pro_response, pro_personality, pro_challenge))

        contra_response = get_response(contra_model, f"Respond concisely to: {pro_response}", contra_personality, contra_challenge)
        print(color.RED + f"\n❌ {contra_model} (Con):\n" + color.END + f"{contra_response}")
        asyncio.run(speak_text(contra_response, contra_personality, contra_challenge))

        pro_argument = pro_response
        contra_argument = contra_response

        round_number += 1
        user_input = input("\nPress Enter for next round or type 'quit' to exit: ").strip().lower()
        if user_input == "quit":
            closing_text = "🎤 Debate ended. Thanks for moderating! 🎤\n"
            spaces = (terminal_width - len(closing_text)) // 2
            print(" " * spaces + color.BOLD + closing_text + color.END)
            break

if __name__ == "__main__":
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

    print(color.BOLD + "\n\nChoose models for the debate (L: Llama3.2, M: Mistral)\n" + color.END)
    
    models = {"L": "llama3.2", "M": "mistral"}
    
    pro_choice = input("Select Pro model (L/M): ").strip().upper()
    if pro_choice not in models:
        print("Invalid choice. Defaulting to Llama3.2 for Pro.")
        pro_model = "llama3.2"
    else:
        pro_model = models[pro_choice]

    contra_choice = "M" if pro_choice == "L" else "L"
    contra_model = models[contra_choice]

    print(f"\n🔥 Debate Setup: {pro_model} (Pro) vs {contra_model} (Con) 🔥\n")
    
    topic = input("Enter the debate topic: ").strip()
    debate_loop(topic, pro_model, contra_model)