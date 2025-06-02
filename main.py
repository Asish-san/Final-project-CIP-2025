import time
import random
import os
from datetime import datetime

# 🌿 MindHaven: A Mindfulness & Mental Fitness program 🌿
# ──────────────────────────────────────────────────────────────
"""
 This program is designed to blend simple IQ exercises with guided
 emotional reflection and mindfulness techniques, aiming to bring
 calmness, awareness, and clarity to users in just a few minutes.
"""
"""
 It starts by welcoming the user warmly and slowly transitions
 through the following steps:
"""
#   1. A light IQ warm-up to engage mental alertness.
#   2. An emotional check-in where users express how they feel.
#   3. A reflective mirror that provides insight and a quote.
#   4. Mood-specific techniques to promote calmness or joy.
#   5. A visual break with calming ASCII scenes and quotes.
#   6. Optional journaling to reflect and store personal thoughts.
#   7. Collects feedback to evaluate user satisfaction.
#   8. Closes with warmth and displays saved journal entries.

# 📌 Why is this important?
""" 
 In our fast-paced world, individuals often lack the space to pause
 and reflect. This app acts like a digital mental pause button—
 offering relaxation, a sense of being heard, and helpful coping
 suggestions—all in a few mindful minutes.
"""
# ✨ Potential impact:
# - Builds emotional awareness and self-reflection habits
# - Reduces stress, improves mood, and increases daily clarity
# - Encourages journaling, which supports mental well-being
# - Combines mental stimulation (IQ) with mindfulness for balance

# Created for anyone needing a short but meaningful reset during their day.

# Global journal to store session notes
journal_entries = []

# Persistent session tracker
session_state = {
    "first_time_user": True
}

# Utility: Clear the console screen for clean transitions
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# Dummy GPT wrapper to simulate AI-generated content in offline mode
def call_gpt(engine, prompt, max_tokens, temperature, n, stop):
    if "IQ questions" in prompt:
        # Returns pre-defined IQ question sets (can be AI-driven later)
        iq_sets = [
            "What is 7 + 5?|12\nWhat comes next: 3, 6, 12, ?|24\nUnscramble 'NAPAEL' to form a country.|NEPAL",
            "What is the square root of 81?|9\nWhich number comes next: 2, 4, 8, 16, ?|32\nWhat is the capital of France?|PARIS",
            "Find the odd one out: Apple, Banana, Carrot, Mango|CARROT\nRearrange 'NAGERM' to form a country.|GERMAN\nWhat is 11 x 3?|33"
        ]
        return {
            "choices": [{
                "text": random.choice(iq_sets)
            }]
        }
    elif "Mind Mirror" in prompt:
        # Returns mindfulness quote
        return {
            "choices": [{
                "text": "“Awareness is the greatest agent for change.” – Eckhart Tolle"
            }]
        }
    else:
        return {"choices": [{"text": ""}]}

# Input wrapper to allow compatibility with restricted environments
def get_input(prompt=""):
    try:
        return input(prompt)
    except OSError:
        return "DUMMY_INPUT"

# Displays welcome screen with calming intro
def welcome_screen():
    clear()
    print("=" * 60)
    print("""
╔════════════════════════════════════════════╗
║            🌿 Welcome to MindHaven 🌿     ║
║     — Tease your brain, calm your mind —   ║
╚════════════════════════════════════════════╝
🧘‍♂️ Prepare to journey through puzzles that:
   • Sharpen focus
   • Slow your breath
   • Guide you gently toward clarity
✨ Let the calm challenge begin...""".center(60))
    print("=" * 60)
    get_input("\n📘 Press Enter to begin your mindfulness journey...")

# Introduces IQ puzzle set to activate the user's mind
def iq_warmup():
    clear()
    print("🧠 Let's begin with a quick IQ warm-up to get your mind engaged.")
    score = 0
# Generates random IQ questions
    questions = generate_iq_questions()

    for i, q in enumerate(questions, 1):
        print(f"\n🔹 Q{i}: {q['q']}")
        ans = get_input("> ").strip().upper()
        if ans == q['a']:
            print("✅ Correct!")
            score += 1
        else:
            print(f"❌ Oops! The correct answer is {q['a']}.")
        time.sleep(1)
    get_input(f"\nYou got {score}/{len(questions)}! Great start. Press Enter to continue...")

# Generate IQ questions via GPT 
def generate_iq_questions():
    prompt = (
        "Generate 3 simple IQ questions with their answers, "
        "each question and answer separated by '|' like: question|answer\n"
        "Make questions about sequences, word puzzles, and basic math."
    )
    response = call_gpt(
        engine="local-dummy",
        prompt=prompt,
        max_tokens=150,
        temperature=0.9,
        n=1,
        stop=None,
    )
    questions = []
    if response:
        text = response["choices"][0]["text"].strip()
        for line in text.split('\n'):
            if '|' in line:
                q, a = line.split('|', 1)
                questions.append({"q": q.strip(), "a": a.strip().upper()})

    return questions

# Emotional check-in: helps users process how they feel and why
def ask_question():
    clear()
    print("\nLet's begin with a simple emotional check-in.")
    feeling = get_input("\n🧠 How are you feeling today?\n> ")
    reason = get_input("\n💬 What do you think is causing this feeling?\n> ")
    print("\n🤖 Based on what you shared, here's a reflection:")
    mood = analyze_input(feeling, reason)
    if mood == "positive":
        print("😊 You're radiating positive vibes. Keep it up!")
    elif mood == "stressed":
        print("😟 It seems like you're facing some stress. Let's find calm together.")
    else:
        print("😐 You're feeling neutral. Let's bring clarity to your day.")
    get_input("\n🌿 Press Enter to continue...")
    display_mind_mirror(feeling, reason)
    return feeling.strip(), reason.strip()

# Display reflective statement with GPT-driven quote
def display_mind_mirror(feeling, reason):
    print("\n🪞 Mind Mirror")
    print(f"💬 You're feeling '{feeling}' because '{reason}'.")
    quote_prompt = f"Mind Mirror: Give a deep, short self-awareness quote."
    quote_resp = call_gpt("local-dummy", quote_prompt, 50, 0.7, 1, None)
    quote = quote_resp["choices"][0]["text"] if quote_resp else "Be here now."
    print(f"🧘‍♀️ Reflect on this:\n🧠 {quote.strip()}")
    get_input("\n💡 Press Enter to continue...")

# Analyses user's mood category using keyword matching
def analyze_input(feeling, reason):
    stress_keywords = ["tired", "sad", "angry", "stressed", "anxious", "worried"]
    positive_keywords = ["happy", "excited", "calm", "relaxed", "good", "great"]

    feeling_lower = feeling.lower()
    if any(word in feeling_lower for word in stress_keywords):
        return "stressed"
    elif any(word in feeling_lower for word in positive_keywords):
        return "positive"
    else:
        return "neutral"

# Based on mood, suggests calming or uplifting mindfulness techniques
def suggest_technique(mood):
    techniques = {
        "stressed": [
            "🌬️ Take a few deep breaths. Inhale... Exhale...",
            "🚶‍♀️ Try a 5-minute walk in nature.",
            "📝 Write down three things you're grateful for.",
            "🎧 Listen to a calming playlist."
        ],
        "positive": [
            "🎉 Keep up the great energy!",
            "💌 Share your joy with someone today.",
            "🌞 Reflect on what's going well right now.",
            "😄 Smile at yourself in the mirror!"
        ],
        "neutral": [
            "🙆 Pause for a moment and stretch your body.",
            "🧘‍♂️ Close your eyes and count to ten slowly.",
            "🔍 Notice 3 things around you that make you feel safe.",
            "📖 Read a short poem or quote you love."
        ]
    }
    clear()
    print("\nAnalyzing your mood...")
    time.sleep(1.5)

    suggestions = random.sample(techniques[mood], 2)
    for i, tip in enumerate(suggestions, 1):
        print(f"\n💡 Tip {i}: {tip}")
        get_input("Press Enter to try this...")

# ASCII-based visual scene with quote to promote mental stillness
def show_calm_graphic():
    clear()
    print("\nTake a moment to relax with this calming scene:\n")
    print("~" * 60)
    print("         🌊   ~   ~      ~      ~    🌊")
    print("     ~       🌴      ~     🌞     ~     ")
    print("         ~       ~      ~     ~       ")
    print("~" * 60)
    time.sleep(2)
    print("\n💬 Here's a quote to reflect on:")
    quotes = [
        "🌟 'This too shall pass.'",
        "💫 'Peace begins with a smile.' – Mother Teresa",
        "🌱 'Breathe. Let go. And remind yourself that this moment is the only one you know you have for sure.'"
    ]
    print(f"\n📖 {random.choice(quotes)}")
    get_input("\n🎧 Press Enter to continue...")

# Offers a journaling opportunity to note feelings or thoughts
def journal_note():
    note = get_input("\n📝 Would you like to write a quick note about today? (optional)\n> ")
    if note.strip():
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        journal_entries.append((timestamp, note.strip()))
        print("✅ Note saved.")
    get_input("Press Enter to continue...")

# Asks for user feedback to understand experience quality
def user_feedback():
    feedback = get_input("\n💭 Did you find this helpful? (yes/no): ")
    get_input("Thank you! Press Enter to finish...")
    return feedback.strip().lower()

# Closes session with personalized message
def closing_message(feedback):
    clear()
    print("\n" + "=" * 60)
    if feedback == "yes":
        print("💚 We're glad it helped! Keep coming back. 💚".center(60))
    else:
        print("🌿 Thanks for trying! Wishing you a calm day. 🌿".center(60))
    print("=" * 60)

# Displays all past journal entries from session
def display_journal():
    if not journal_entries:
        print("\n📓 No notes yet.")
    else:
        print("\n🗂️ Your Journal Entries:")
        for time_stamp, note in journal_entries:
            print(f"\n[{time_stamp}]\n📝 {note}")

# 🔁 The main program execution loop (Main function starts from here)
def run_mindfulness_game():
    welcome_screen()
    iq_warmup()
    feeling, reason = ask_question()
    mood = analyze_input(feeling, reason)
    suggest_technique(mood)
    show_calm_graphic()
    journal_note()
    feedback = user_feedback()
    closing_message(feedback)
    display_journal()

# 🚀 Entry point of the program
if __name__ == "__main__":
    run_mindfulness_game()
    
