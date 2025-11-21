import tkinter as tk
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle  # Assuming tokenizer was saved during model training

class AndroidKeyboard(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Android Keyboard")
        self.geometry("600x400")
        self.configure(bg='#2E2E2E')  # Dark grayish background for the main window

        # Load trained model and tokenizer
        self.model = tf.keras.models.load_model('nexpree1.keras')
        with open('tokenizer.pkl', 'rb') as handle:  # Ensure tokenizer was saved during training
            self.tokenizer = pickle.load(handle)
        
        self.max_length = 107  # Based on training data (maximum sequence length)

        # Display area for word recommendations
        self.recommendations_frame = tk.Frame(self, height=2, pady=10, bg='#3A3A3A')
        self.recommendations_frame.pack(fill="x")
        
        # Label to display next word recommendations
        self.recommendations_label = tk.Label(
            self.recommendations_frame, 
            text="Recommendations: ", 
            font=("Helvetica", 14), 
            bg='#3A3A3A', 
            fg='white'
        )
        self.recommendations_label.pack()

        self.recommendations_buttons = []  # To dynamically manage recommendation buttons

        # Input field with dark background
        self.input_field = tk.Entry(self, font=("Helvetica", 16), width=40, bg='#2E2E2E', fg='white', insertbackground='white')
        self.input_field.pack(pady=10)
        self.input_field.bind("<space>", self.show_recommendations)  # Show predictions after space
        self.input_field.bind("<Control-BackSpace>", self.ctrl_backspace)  # Bind Ctrl+Backspace event
        self.input_field.bind("<BackSpace>", self.dynamic_recommendations)  # Bind Backspace for dynamic recommendations
        
        # Keyboard frame with dark background
        self.keyboard_frame = tk.Frame(self, bg='#2E2E2E')
        self.keyboard_frame.pack()

        # Define keyboard layout
        self.keys_layout = [
            ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
            ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
            ['z', 'x', 'c', 'v', 'b', 'n', 'm'],
            ['space', 'backspace']
        ]
        
        # Build the keyboard buttons
        self.build_keyboard()
    
    def build_keyboard(self):
        for row_index, row in enumerate(self.keys_layout):
            row_frame = tk.Frame(self.keyboard_frame, bg='#2E2E2E')
            row_frame.pack(side="top")
            
            for key in row:
                if key == 'space':
                    btn = tk.Button(
                        row_frame, text="SPACE", width=20, height=2, 
                        command=lambda k=key: self.press_key(k), 
                        bg='#4A4A4A', fg='white', activebackground='#555555'
                    )
                elif key == 'backspace':
                    btn = tk.Button(
                        row_frame, text="BACKSPACE", width=8, height=2, 
                        command=lambda k=key: self.press_key(k), 
                        bg='#4A4A4A', fg='white', activebackground='#555555'
                    )
                else:
                    btn = tk.Button(
                        row_frame, text=key.upper(), width=5, height=2, 
                        command=lambda k=key: self.press_key(k), 
                        bg='#4A4A4A', fg='white', activebackground='#555555'
                    )
                
                btn.pack(side="left", padx=2, pady=2)
    
    def press_key(self, key):
        if key == 'space':
            self.input_field.insert(tk.END, ' ')
            self.show_recommendations()
        elif key == 'backspace':
            current_text = self.input_field.get()
            if current_text.endswith(" "):  # If last character is a space, update recommendations
                self.dynamic_recommendations()
            self.input_field.delete(len(current_text) - 1)
        else:
            self.input_field.insert(tk.END, key)
    
    def ctrl_backspace(self, event=None):
        """Handle Ctrl+Backspace to delete the last word."""
        current_text = self.input_field.get().rstrip()  # Remove trailing spaces
        if current_text:
            new_text = ' '.join(current_text.split()[:-1])  # Remove the last word
            self.input_field.delete(0, tk.END)
            self.input_field.insert(0, new_text)
            self.dynamic_recommendations()

    def show_recommendations(self, event=None):
        """Show next-word recommendations based on the entire input sentence."""
        text = self.input_field.get().strip()  # Full input sentence
        recommendations = self.get_recommendations(text)
        self.display_recommendations(recommendations)

    def dynamic_recommendations(self, event=None):
        """Dynamically update recommendations based on the full input sentence."""
        text = self.input_field.get().strip()
        recommendations = self.get_recommendations(text)
        self.display_recommendations(recommendations)

    def get_recommendations(self, sentence):
        """Get next-word predictions from the trained model based on the entire sentence."""
        if sentence:
            sequence = self.tokenizer.texts_to_sequences([sentence])  # Tokenize the full sentence
            padded_sequence = pad_sequences(sequence, maxlen=self.max_length, padding='pre')  # Pad to match model input
            predictions = self.model.predict(padded_sequence)[0]  # Predict for the sequence
            top_indices = np.argsort(predictions)[-4:][::-1]  # Get top 4 predictions
            return [self.tokenizer.index_word.get(i, "<UNK>") for i in top_indices]
        return []

    def display_recommendations(self, recommendations):
        """Display recommendations as clickable buttons."""
        # Clear existing recommendation buttons
        for btn in self.recommendations_buttons:
            btn.destroy()
        self.recommendations_buttons = []

        # Create new recommendation buttons
        for word in recommendations:
            btn = tk.Button(
                self.recommendations_frame, text=word, font=("Helvetica", 14),
                bg='#3A3A3A', fg='white', activebackground='#555555',
                command=lambda w=word: self.insert_recommendation(w)
            )
            btn.pack(side="left", padx=5)
            self.recommendations_buttons.append(btn)

    def insert_recommendation(self, word):
        """Insert the selected recommendation into the input field."""
        current_text = self.input_field.get().strip()
        if current_text and not current_text.endswith(" "):
            current_text += " "
        self.input_field.delete(0, tk.END)
        self.input_field.insert(0, current_text + word + " ")
        self.show_recommendations()


