# FridgeMate

> **Find recipes using ingredients you already have — right from your desktop.**

FridgeMate is a desktop application that lets you search for recipes using the ingredients sitting in your fridge. It uses a fuzzy-matching engine under the hood, so you don't need to spell everything perfectly. Just type what you have and FridgeMate finds the best-matching recipes, ranked by how many ingredients you already own.

---

## Features

- **Ingredient-based recipe search** — type in what you have, get recipes that match
- **Fuzzy matching** — handles typos and partial names (e.g. "onion" matches "spring onion")
- **Match percentage** — see how well each recipe fits your available ingredients
- **Ingredient checker** — visual indicators show which ingredients you have vs. which you're missing
- **Recent searches** — quickly re-run your past ingredient searches for the session
- **Step-by-step instructions** — detailed cooking steps for every recipe

---

## 🗂️ Project Structure

```
fridgemate/
├── main.py                  # App entry point — launches the WebUI window
├── requirements.txt         # Python dependencies
│
├── backend/
│   ├── engine.py            # Core recipe search & scoring logic
│   └── matcher.py           # Fuzzy ingredient matching algorithm
│
├── database/
│   └── resep.json           # Recipe database (50 recipes)
│
└── frontend/
    ├── home.html            # Home page — ingredient input & recent searches
    ├── recipes.html         # Search results — recipe cards with match %
    ├── open card.html       # Recipe detail — ingredients & step-by-step guide
    ├── style.css            # App-wide styles
    ├── webui.js             # WebUI bridge (auto-served by the backend)
    └── images/              # Recipe images (id-1.jpg, id-2.jpg, ...)
```

---

## Requirements

- **Python 3.8+**
- **pip** (comes bundled with Python)

---

## How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/mieraaaa/fridgemate.git
cd fridgemate
```

> Make sure you are on the **`main`** branch:
> ```bash
> git checkout main
> ```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs the `webui2` library which powers the desktop window.

### 3. Launch the App

```bash
python main.py
```

A native desktop window will open automatically with FridgeMate. 🎉

---

## How to Use

1. **Home Page**: Type an ingredient into the search bar and press **Enter** to add it as a tag. Add as many ingredients as you like.
2. **Search**: Press the **"Let's Cook!"** button to search for matching recipes.
3. **Results Page**: Browse the list of recipes ranked by match percentage. Each card shows how many ingredients are needed and how many you already have.
4. **Recipe Detail**: Tap any recipe card to view the full details — including an ingredients checklist (✅ available / ⬜ missing) and numbered cooking steps.
5. **Go Back**: Use the **←** back arrow in the top-left to return to the previous screen.
6. **Recent Searches**: Your last few searches are saved for the session and shown on the home page for quick re-use.

---

## How It Works

FridgeMate uses [WebUI](https://webui.me/) (`webui2`) to serve the HTML frontend as a native desktop application. Communication between the browser-based UI and the Python backend happens over a local WebSocket bridge.

```
[User Input (HTML)] 
      ↕ webui.call()
[Python Backend (main.py)]
      ↕ engine.py
[Fuzzy Matcher (matcher.py)]
      ↕
[Recipe Database (resep.json)]
```

The **fuzzy matcher** uses Python's built-in `difflib.SequenceMatcher` to handle typos and partial matches with a configurable similarity threshold (default: 70%).

---

## Dependencies

| Package | Purpose |
|---------|---------|
| `webui2` | Desktop window + Python↔HTML bridge |

Install with:
```bash
pip install webui2
```

---



