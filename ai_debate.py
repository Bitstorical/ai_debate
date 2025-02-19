import ollama
import random
import shutil
import os

PERSONALITIES = ["a strict professor", "a passionate politician", "a sarcastic comedian", "a data-driven scientist"]
CHALLENGES = ["Use historical facts only.", "Use sports metaphors.", "Make it sound dramatic.", "Limit response to 1 sentence."]

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

def get_response(model, prompt, personality, challenge):
    """Query the LLM with personality and challenge constraints."""
    try:
        full_prompt = f"You are {personality}. {challenge} Keep your response to one concise sentence. Debate the following: {prompt}"
        response = ollama.chat(model=model, messages=[{"role": "user", "content": full_prompt}])
        return response['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"

def debate_loop(topic, pro_model, contra_model):
    """Handles the debate logic with argument exchanges, personalities, and challenges."""
    
    # bissle UX :) create a frame 
    terminal_width = shutil.get_terminal_size().columns
    line = "-" * terminal_width

    text_debate= f"🔥 Debate on: {topic} 🔥\n"
    spaces = (terminal_width - len(text_debate)) // 2
    
    print(line)
    print(" " * spaces+ color.BOLD + text_debate + color.END)
    
    spaces = (terminal_width - len("Round")) // 2
    
    pro_personality = random.choice(PERSONALITIES)
    contra_personality = random.choice(PERSONALITIES)
    pro_challenge = random.choice(CHALLENGES)
    contra_challenge = random.choice(CHALLENGES)
    
    pro_argument = f"I support {topic} because..."
    contra_argument = f"I oppose {topic} because..."

    spaces = (terminal_width - len("Round")) // 2 # for centtering the Round x: text
  
    round_number = 1 #reset round number 
    while True:
        print(line)
        print(" " * spaces+ color.BOLD + f"🔄 Round {round_number}:\n" + color.END)
        print(f"🎭 {pro_model} (Pro) "+ color.UNDERLINE+ f"is {pro_personality}"+ color.END + f"| ⚡ Challenge: {pro_challenge}")
        print(f"🎭 {contra_model} (Con) "+ color.UNDERLINE+ f"is {contra_personality} "+ color.END + f"| ⚡ Challenge: {contra_challenge}\n\n")
       
        # Pro side responds based on Contra's last argument
        pro_response = get_response(pro_model, f"Respond concisely to: {contra_argument}", pro_personality, pro_challenge)
        print(color.GREEN +f"✅ {pro_model} (Pro): \n"+ color.END + f"{pro_response}")

        # Contra side responds based on Pro's last argument
        contra_response = get_response(contra_model, f"Respond concisely to: {pro_response}", contra_personality, contra_challenge)
        print(color.RED +f"\n❌ {contra_model} (Con):\n"+ color.END + f"{contra_response}")
     
        # Update arguments for next round
        pro_argument = pro_response
        contra_argument = contra_response

        round_number += 1
        user_input = input("\nPress Enter for next round or type 'quit' to exit: ").strip().lower()
        if user_input == "quit":
             
            #center closing text 
            closing_text="🎤 Debate ended. Thanks for moderating! 🎤\n"
            spaces = (terminal_width - len(closing_text)) // 2
            print(" " * spaces+ color.BOLD +closing_text + color.END)

            break

if __name__ == "__main__":
   
    # Clear screen for Windows
    if os.name == 'nt':
        os.system('cls')
    # Clear screen for macOS and Linux
    else:
        os.system('clear')

    print(color.BOLD +"\n\nChoose models for the debate (L: Llama3.2, M: Mistral)\n"+ color.END)
    
    models = {"L": "llama3.2", "M": "mistral"}
    
    pro_choice = input("Select Pro model (L/M): ").strip().upper()
    if pro_choice not in models:
        print("Invalid choice. Defaulting to Llama3.2 for Pro.")
        pro_model = "llama3.2"
    else:
        pro_model = models[pro_choice]

    contra_choice = "M" if pro_choice == "L" else "L"  # Assign the other model automatically
    contra_model = models[contra_choice]

    print(f"\n🔥 Debate Setup: {pro_model} (Pro) vs {contra_model} (Con) 🔥\n")
    
    topic = input("Enter the debate topic: ").strip()
    debate_loop(topic, pro_model, contra_model)