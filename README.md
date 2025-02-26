# AI Debate Simulator

## 🚀 Overview
Welcome to the **AI Debate Simulator**, where two powerful LLMs—**Llama3.2** and **Mistral**—go head-to-head in a structured debate while you moderate the discussion! The models exchange arguments based on a given topic, adopting unique **personalities** and facing fun **challenges** for an engaging and unpredictable debate. 

## 🎯 Features
- **Choose Your AI Debaters**: Select which model takes the **Pro** or **Con** side (L for Llama, M for Mistral).
- **Live Argument Exchange**: Each AI responds to the opponent's last argument, ensuring a continuous discussion.
- **Personalities & Challenges**: Add spice with roles like **'a sarcastic comedian'** or constraints like **'use only historical facts'**.
- **Threaded Execution**: Both models run independently in **separate threads via Ollama**, ensuring smooth operation.
- **Simple Terminal Interface**: Type a topic and moderate the debate round-by-round!
- **Microsoft Edge’s online text-to-speech service for argument speech synthesis.**:

## 🛠️ Installation & Setup
### 1️⃣ Install Ollama
Ensure you have [Ollama](https://ollama.ai/) installed on your system.

```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### 2️⃣ Pull the Required Models
Download **Llama3.2** and **Mistral** via Ollama:

```bash
ollama pull llama3.2
ollama pull mistral
```

### 3️⃣ Run the Debate Simulator
Clone the repository and run the script:

```bash
git clone git clone https://github.com/Bitstorical/ai_debate
cd ai-debate-simulator
python ai_debate.py
```

## 🎮 How to Play
1. **Choose a Debate Topic**: Enter a topic, and the AI will start arguing!
2. **Select Pro & Con Models**: Type `L` for Llama, `M` for Mistral.
3. **Watch the Debate Unfold**: Each AI exchanges arguments based on the opponent’s last point.
4. **Spice It Up**: Introduce **personalities** or **challenges** for unexpected twists.
5. **Quit Anytime**: Type `quit` to end the session.

## 🏆 Example Debate Session

![grafik](https://github.com/user-attachments/assets/4d9b9525-ceff-4c44-916f-d658086815d9)

```
🔥 Debate on: "Should AI replace human artists?" 🔥

Pro (Llama): "AI enhances creativity by automating tedious tasks."
Con (Mistral): "Creativity is inherently human and irreplaceable."

Pro (Llama): "AI can generate unique, never-before-seen artworks."
Con (Mistral): "But it lacks emotion and true artistic intent."
...
```

## 📜 System Architecture
- **Ollama** runs both LLMs locally.
- **Multi-threading** allows independent execution of the debate participants.
- **Dynamic Argument Exchange**: Each AI responds to the latest opponent’s point.

## 🤖 Future Enhancements
- More LLMs and personality packs.
- Extended challenge sets for even wilder debates.
- Web-based UI for a visual debate experience.

## 🎉 Join the Debate!
Try it out and let the AI battle begin! ⚔️🔥

#AI #Debate #MachineLearning #Ollama #TechFun
