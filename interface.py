import json
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import tkinter as tk
from tkinter import scrolledtext

# Ajouter le chemin pour les ressources NLTK (si nécessaire)
nltk.data.path.append('C:\\Users\\laana\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\site-packages\\nltk')

# Télécharger les ressources nécessaires
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

# Charger la base de connaissances
def load_knowledge_base(file):
    try:
        with open(file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Erreur : le fichier 'knowledge_base.json' est introuvable.")
        exit()
    except json.JSONDecodeError:
        print("Erreur : le fichier 'knowledge_base.json' est mal formé.")
        exit()

# Fonction de prétraitement du texte
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  # Retirer la ponctuation
    text = text.strip()
    
    # Tokenization
    tokens = nltk.word_tokenize(text)
    
    # Suppression des stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    
    return tokens

# Trouver la meilleure réponse
def find_best_response(question_tokens, knowledge_base):
    question_text = ' '.join(question_tokens)  # Rejoindre les tokens en texte
    for item in knowledge_base["questions"]:
        processed_question = preprocess_text(item["question"])
        if question_text in ' '.join(processed_question):  # Comparer avec les versions prétraitées
            return item["response"]
    return "Sorry I don't have answer ."

# Interface graphique Tkinter
def create_chat_gui():
    # Charger la base de connaissances
    knowledge_base = load_knowledge_base('knowledge_base.json')
    
    # Fonction pour traiter l'envoi des messages
    def on_send_button_click():
        user_input = user_input_field.get().strip()  # Récupérer l'entrée utilisateur
        if not user_input:
            return
        #condition d'arret 
        if user_input.lower() == "exit":
            window.quit()  # Fermer la fenêtre Tkinter
            return
        
        # Afficher le message utilisateur
        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END, "Vous: " + user_input + "\n", "user")
        
        # Prétraiter et répondre à la question
        question_processed = preprocess_text(user_input)
        response = find_best_response(question_processed, knowledge_base)
        
        # Afficher la réponse du chatbot
        chat_display.insert(tk.END, "LIZA: " + response + "\n", "bot")
        chat_display.config(state=tk.DISABLED)
        
        # Effacer le champ de saisie
        user_input_field.delete(0, tk.END)

    # Fonction pour envoyer le message avec la touche "Entrée"
    def on_enter_key(event):
        on_send_button_click()

    # Créer la fenêtre principale
    window = tk.Tk()
    window.title("LIZA - Chatbot")
    
    # Créer le widget d'affichage des messages avec défilement
    chat_display = scrolledtext.ScrolledText(window, height=20, width=50, state=tk.DISABLED, wrap=tk.WORD)
    chat_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
    
    # Configurer les styles des messages
    chat_display.tag_configure("user", foreground="blue", font=("Arial", 10, "bold"))
    chat_display.tag_configure("bot", foreground="green", font=("Arial", 10, "italic"))

    # Ajouter le message d'introduction
    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, "LIZA: Hello, I'm your  chatbot Liza. put me some question to help you or tape  'exit' to quit .\n", "bot")
    chat_display.config(state=tk.DISABLED)

    # Créer le champ de saisie utilisateur
    user_input_field = tk.Entry(window, width=40)
    user_input_field.grid(row=1, column=0, padx=10, pady=10)
    user_input_field.bind("<Return>", on_enter_key)  # Lier "Entrée" pour envoyer
    
    # Créer le bouton "Envoyer"
    send_button = tk.Button(window, text="send", command=on_send_button_click, width=10, bg="#4CAF50", fg="white")
    send_button.grid(row=1, column=1, padx=10, pady=10)

    # Démarrer la boucle d'événements Tkinter
    window.mainloop()

# Exécuter le chatbot avec interface
if __name__ == "__main__":
    create_chat_gui()
