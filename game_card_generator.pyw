#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox, filedialog, colorchooser
from google import genai
import json
import webbrowser
import os
import datetime
import random
import re
import threading

# ==========================================
# ENTER YOUR API KEY HERE
# Get one at: https://aistudio.google.com/
# ==========================================
API_KEY = "YOUR_API_KEY_HERE"

class GameCardGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Card Generator")
        self.root.geometry("600x650")
        
        # Locate the directory where this script lives
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(self.script_dir, "used_words.json")

        # Load persistent database from file
        self.session_words = self.load_database()
        
        # Default save directory (where the script is located)
        self.output_dir = self.script_dir
        
        # Default card color (White)
        self.card_color = "#ffffff"

        # Configure Client using the new SDK standard
        self.client = genai.Client(api_key=API_KEY)

        self.setup_ui()

    def load_database(self):
        """Loads used words from used_words.json if it exists."""
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return set(data)
            except Exception as e:
                print(f"Failed to load database: {e}")
                return set()
        return set()

    def save_database(self):
        """Saves current word set to used_words.json."""
        try:
            with open(self.db_path, "w", encoding="utf-8") as f:
                json.dump(sorted(list(self.session_words)), f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Failed to save database: {e}")

    def setup_ui(self):
        # --- Save Location Section ---
        tk.Label(self.root, text="Save Location:", font=("Arial", 10, "bold")).pack(pady=(10, 0))
        
        dir_frame = tk.Frame(self.root)
        dir_frame.pack(pady=5)
        
        self.dir_label = tk.Label(dir_frame, text=self.output_dir, fg="blue", wraplength=400)
        self.dir_label.pack(side="left", padx=10)
        
        tk.Button(dir_frame, text="Browse...", command=self.choose_directory).pack(side="left")

        # --- Divider ---
        tk.Frame(self.root, height=1, bg="grey").pack(fill="x", padx=20, pady=10)

        # --- Instructions & Presets ---
        tk.Label(self.root, text="Card Category / Search Criteria:", font=("Arial", 12, "bold")).pack()
        
        preset_frame = tk.Frame(self.root)
        preset_frame.pack(pady=10)
        
        # Quick-fill suggestion buttons
        tk.Button(preset_frame, text="Pop Culture & Tech", command=lambda: self.set_preset("General pop culture, geography, and technology")).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(preset_frame, text="Nature & Science", command=lambda: self.set_preset("The natural world, biology, outer space, and chemistry")).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(preset_frame, text="Sports & Entertainment", command=lambda: self.set_preset("Famous sports, movies, music genres, and hobbies")).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(preset_frame, text="Random Mix", command=lambda: self.set_preset("A completely random mix of history, food, everyday objects, and animals")).grid(row=1, column=1, padx=5, pady=5)

        # Input field
        self.criteria_entry = tk.Entry(self.root, width=55, font=("Arial", 12))
        self.criteria_entry.pack(pady=5)
        self.criteria_entry.insert(0, "General pop culture, geography, and technology")

        # --- Divider ---
        tk.Frame(self.root, height=1, bg="grey").pack(fill="x", padx=20, pady=10)

        # --- Color Picker Section ---
        color_frame = tk.Frame(self.root)
        color_frame.pack(pady=5)
        
        tk.Label(color_frame, text="Card Background Color:", font=("Arial", 10, "bold")).pack(side="left", padx=5)
        
        self.color_preview = tk.Label(color_frame, text="      ", bg=self.card_color, relief="solid", borderwidth=1)
        self.color_preview.pack(side="left", padx=5)
        
        tk.Button(color_frame, text="Pick Color", command=self.choose_color).pack(side="left", padx=5)

        # --- Generate Button ---
        self.generate_btn = tk.Button(self.root, text="Generate 1 New Page (16 Cards)", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", command=self.start_generation_thread)
        self.generate_btn.pack(pady=20)

        # Status Label
        self.status_label = tk.Label(self.root, text=f"Total words in persistent database: {len(self.session_words)}", fg="gray")
        self.status_label.pack(side="bottom", pady=10)

    def choose_directory(self):
        selected_dir = filedialog.askdirectory(initialdir=self.output_dir, title="Select Save Folder")
        if selected_dir:  
            self.output_dir = selected_dir
            self.dir_label.config(text=self.output_dir)

    def set_preset(self, text):
        self.criteria_entry.delete(0, tk.END)
        self.criteria_entry.insert(0, text)

    def choose_color(self):
        color_code = colorchooser.askcolor(title="Choose Card Background Color", initialcolor=self.card_color)[1]
        if color_code:  
            self.card_color = color_code
            self.color_preview.config(bg=self.card_color)

    def start_generation_thread(self):
        if API_KEY == "YOUR_API_KEY_HERE":
            messagebox.showerror("Error", "Please insert your API Key at the top of the script!")
            return

        criteria = self.criteria_entry.get()
        if not criteria:
            messagebox.showwarning("Warning", "Please enter some search criteria.")
            return

        self.generate_btn.config(text="Generating... Please wait", state="disabled")
        threading.Thread(target=self._process_generation, args=(criteria,), daemon=True).start()

    def _process_generation(self, criteria):
        try:
            prompt = f"""
            Generate exactly 80 unique, distinct nouns/concepts for a party guessing game based on these criteria: {criteria}.
            The words must be fun to describe and guess. 
            DO NOT include any of these words: {list(self.session_words)}.
            Respond ONLY with a raw JSON array of 80 strings. Do not include markdown formatting or the word 'json'.
            """

            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            
            raw_text = response.text.strip()
            if raw_text.startswith("```json"):
                raw_text = raw_text[7:]
            if raw_text.startswith("```"):
                raw_text = raw_text[3:]
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]

            new_words = json.loads(raw_text.strip())

            if len(new_words) < 80:
                raise ValueError("AI did not generate enough words.")

            final_words = new_words[:80]
            random.shuffle(final_words)

            self.root.after(0, lambda: self._finalize_generation(final_words, criteria))

        except Exception as e:
            self.root.after(0, lambda error=e: self._generation_error(error))

    def _finalize_generation(self, words, criteria):
        # Update set and save to database file
        self.session_words.update(words)
        self.save_database()
        
        self.status_label.config(text=f"Total words in persistent database: {len(self.session_words)}")

        # Create the HTML file
        self.create_html_file(words, criteria, self.card_color)
        
        self.generate_btn.config(text="Generate 1 New Page (16 Cards)", state="normal")
        messagebox.showinfo("Success", "Cards generated! Opening in your browser for printing.")

    def _generation_error(self, error):
        self.generate_btn.config(text="Generate 1 New Page (16 Cards)", state="normal")
        messagebox.showerror("Error", f"Failed to generate cards. Ensure your API key is correct.\n\nDetails: {error}")

    def create_html_file(self, words, criteria, color):
        clean_slug = re.sub(r'[^a-z0-9]+', '_', criteria.lower()).strip('_')
        if len(clean_slug) > 40:
            clean_slug = clean_slug[:40].rstrip('_')

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cards_{timestamp}_{clean_slug}.html" if clean_slug else f"cards_{timestamp}.html"
        file_path = os.path.join(self.output_dir, filename)

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<!-- GENERATED WITH PROMPT: {criteria} | COLOR USED: {color} -->
<meta charset="UTF-8">
<title>Game Card Generator</title>
<style>
  @page {{ size: A4 landscape; margin: 0; }}
  body {{ font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f0f0f0; }}
  .page {{ width: 297mm; height: 210mm; background: white; margin: 0 auto; display: flex; justify-content: center; align-items: center; box-sizing: border-box; padding: 10mm; }}
  .grid {{ display: grid; grid-template-columns: repeat(4, 1fr); grid-template-rows: repeat(4, 1fr); width: 100%; height: 100%; border-top: 1px dashed #ccc; border-left: 1px dashed #ccc; }}
  .card {{ background-color: {color}; border-right: 1px dashed #ccc; border-bottom: 1px dashed #ccc; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; padding: 5mm; box-sizing: border-box; }}
  .word {{ font-size: 13pt; font-weight: bold; margin: 2px 0; text-transform: uppercase; line-height: 1.1; }}
</style>
</head>
<body data-prompt="{criteria}" data-color="{color}">
<div class="page"><div class="grid">
"""

        for i in range(0, 80, 5):
            html_content += '<div class="card">'
            for j in range(5):
                if i + j < len(words):
                    html_content += f'<div class="word">{words[i+j]}</div>'
            html_content += '</div>'

        html_content += """
</div></div>
</body>
</html>
"""

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        webbrowser.open(f"file://{file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GameCardGeneratorApp(root)
    root.mainloop()