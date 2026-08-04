# Game Card Generator (Compatible with 30 Seconds)



Game Card Generator is a lightweight, asynchronous desktop application designed to generate print-ready word sheets compatible with fast-paced, 30-second description board games.

> **Disclaimer:** This project is an independent utility and is not affiliated with, endorsed by, or associated with the official *30 Seconds* board game or its trademark holders. It utilizes Nominative Fair Use to describe compatibility.
> 
> 

Built with Python, Tkinter, and the modern Google Gemini API (`google-genai`), the app delivers endless variety straight to a beautifully formatted, print-ready A4 landscape HTML grid.

---

## Features

* **Multi-Threaded Performance:** Generating cards happens entirely in a background thread, ensuring the desktop interface never freezes or marks itself as "Not Responding" while waiting for the AI.


* **Guaranteed Topic Mixing:** Combines advanced AI categorization with Python's hardware-level list randomization so every single printed card features a perfectly unpredictable mix of subjects.


* **Persistent Word Database (`used_words.json`):** Tracks all generated terms locally on disk. Unlike temporary session memory, your word history persists across application restarts to guarantee zero duplicate words over days, weeks, or months of use.
* **Batch Page Generation:** Generate multiple unique card pages in a single run by setting the desired page count. Database memory updates live between each iteration within the batch run.
* **Persistent Color Favorites (`favorites.json`):** Pick custom card background colors with an integrated color chooser and save your favorite swatches across sessions for quick access.
* **Quick-Select Presets:** Includes one-click generation categories alongside full manual text entry (supporting standard copy/paste shortcuts).


* **Memory-Optimized File Export:** Saves HTML sheets directly to your designated output directory without forcibly opening multiple browser tabs, preventing system RAM exhaustion during large batch runs.
* **Smart File Architecture:** Auto-saves unique, chronologically structured files to a custom folder of your choice, ensuring your files sort perfectly by date and time (with batch page numbering).


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

Duplicates are handled programmatically by comparing generated terms against `used_words.json`, which resides in the same folder as the app. On every request, the accumulated word history is passed directly into the AI prompt with strict exclusion instructions. When new words are generated, `used_words.json` is automatically updated and saved.

### Q: Is there a limit to how many words `used_words.json` can hold before the app becomes sluggish?

While Python reads `used_words.json` almost instantaneously regardless of size, performance is bound by the **API prompt payload size**, because all previously used words must be sent to Gemini for exclusion:

* **0 to 5,000 words (~60 pages / 960 cards):** Generation speeds remain fast and responsive.
* **5,000 to 10,000 words (~125 pages):** Small, noticeable latency increase (1–3 extra seconds per page) as Gemini processes larger prompt payloads.
* **10,000+ words:** Requests will slow down noticeably due to high token count pre-processing.

**Tip:** If generation starts to feel sluggish after extensive long-term use, simply delete or rename `used_words.json` to reset the exclusion cache.

### Q: How do I manage my Color Favorites?

* **Add a Color:** Pick a color using **Pick Color**, then click **+ Add to Favourites**. The hex code is saved to `favorites.json`.
* **Select a Favorite:** Left-click any color swatch to instantly set it as your active card background.
* **Remove a Favorite:** Right-click (or two-finger tap on macOS trackpads) any color swatch to delete it from your stored favorites.

### Q: Why don't generated HTML files open in my browser automatically anymore?

Automatic browser launching was disabled to prevent system memory overload when generating multi-page batches (e.g., generating 10–20 pages at once would open 10–20 browser tabs simultaneously). Completed HTML pages are saved directly to your chosen save directory, and a completion window confirms their location.

### Q: How do I know what prompt was used to make an old HTML sheet?

Every output file is stamped in two distinct ways to make tracking and recreating results easy:

1. **The Filename:** Files use the structure `cards_YYYYMMDD_HHMMSS_page1_your_prompt_slug.html`. This places them in strict chronological order while displaying the page index and core topics.
2. **The Source Code:** If you right-click an output HTML file and open it in a text editor like Notepad++, the exact, unedited prompt is hardcoded directly at the top of the file inside an HTML comment (`<!-- GENERATED WITH PROMPT: ... -->`) and as a `data-prompt` attribute inside the `<body>` tag for seamless file indexing.

```