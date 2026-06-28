# Game Card Generator (Compatible with 30 Seconds)

Game Card Generator is a lightweight, asynchronous desktop application designed to generate print-ready word sheets compatible with fast-paced, 30-second description board games. 

> **Disclaimer:** This project is an independent utility and is not affiliated with, endorsed by, or associated with the official *30 Seconds* board game or its trademark holders. It utilizes Nominative Fair Use to describe compatibility.

Built with Python, Tkinter, and the modern Google Gemini API (`google-genai`), the app delivers endless variety straight to a beautifully formatted, print-ready A4 landscape HTML grid.

---

## Features

* **Multi-Threaded Performance:** Generating cards happens entirely in a background thread, ensuring the desktop interface never freezes or marks itself as "Not Responding" while waiting for the AI.
* **Guaranteed Topic Mixing:** Combines advanced AI categorization with Python's hardware-level list randomization so every single printed card features a perfectly unpredictable mix of subjects.
* **Persistent Session Memory:** The app tracks all generated terms in RAM during an active session, ensuring you get zero duplicate words across multiple card sheets.
* **Quick-Select Presets:** Includes one-click generation categories alongside full manual text entry (supporting standard copy/paste shortcuts).
* **Smart File Architecture:** Auto-saves unique, chronologically structured files to a custom folder of your choice, ensuring your files sort perfectly by date and time.
* **Embedded Metadata:** Automatically stamps your exact generation prompt inside the HTML source code as both a comment and a data attribute for instant lookup and organization.

---

## Prerequisites & Installation

### 1. Install Python
Ensure you have **Python 3.10 or higher** installed on your machine. During the Windows installation, make sure to check the box that says **"Add Python to PATH"**.

### 2. Install the Google GenAI SDK
Open your terminal or Command Prompt (`cmd`) and run the following command to install the official SDK:

```bash
pip install google-genai

```

### 3. Acquire an API Key

Grab a free API key from [Google AI Studio](https://aistudio.google.com/) and paste it into the designated `API_KEY` variable at the top of the script file.

---

## How to Run the Application

### On Windows

The script is saved with a `.pyw` extension (`game_card_generator.pyw`). This tells Windows to launch it using `pythonw.exe`, allowing you to double-click the file to open the graphical dashboard instantly without an annoying black command prompt window hanging open in the background.

### On Linux

Linux desktop environments ignore the `.pyw` extension and require execution privileges.

1. Open the file and ensure the python shebang is at the very top line: `#!/usr/bin/env python3`
2. Open your terminal, navigate to the folder, and make the script executable:
```bash
chmod +x game_card_generator.pyw

```


3. You can now double-click to execute or launch it via your local desktop environment shortcut.

---

## Frequently Asked Questions & Project Insights

### Q: Does this application work offline?

**No.** `google-genai` is a cloud-based library. The application does not process the text locally; it securely packages your search criteria and handles the computational generation on Google’s remote servers. An active internet connection is required to create new cards.

### Q: Is there a maximum word limit for the search criteria?

**Practically, no.** While it is best to keep prompts concise for accurate card topics, the underlying model (`gemini-2.5-flash`) possesses a massive context window capable of processing tens of thousands of words. You can be as descriptive or specific with your custom categories as you like.

### Q: How are duplicate words avoided?

Duplicates are handled programmatically through a Python `set()`. While the application is open, every successfully generated word is permanently memorized in RAM. On subsequent clicks, this historical list is passed directly to the AI instructions with strict exclusion rules. (Note: Closing or restarting the application completely flushes this memory cache, giving you a fresh slate).

### Q: How do I know what prompt was used to make an old HTML sheet?

Every output file is stamped in two distinct ways to make tracking and recreating results easy:

1. **The Filename:** Files use the structure `cards_YYYYMMDD_HHMMSS_your_prompt_slug.html`. This places them in strict chronological order while displaying the core topics.
2. **The Source Code:** If you right-click an output HTML file and open it in a text editor like Notepad++, the exact, unedited prompt is hardcoded directly at the top of the file inside an HTML comment (``) and as a `data-prompt` attribute inside the `<body>` tag for seamless file indexing.

### Q: If I put my laptop into Hibernation, will my unique word session break?

**No.** Hibernation completely freezes the state of your computer's RAM and writes it safely to your storage drive. When you wake your computer up, the Python process resumes exactly where it left off, and your session memory remains completely intact.

```

```