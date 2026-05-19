# Life Manager V1

A desktop life management app built with Python and CustomTkinter.  
The project currently includes streak tracking and goal management, with local SQLite storage.

## Features

- Create and manage streaks
- Track completed days
- View streak progress visually
- Manage personal goals
- Local SQLite database storage
- Theme swapability

## Tech Stack

- Python
- CustomTkinter
- SQLite
- Pillow

## Project Structure

```txt
life-management/
├── .gitignore
├── life_manager.db
├── main.py
├── README.md
├── requirements.txt
│
├── backend/
│   ├── database.py
│   ├── services.py
│   ├── classes/
│   │   ├── goal.py
│   │   └── streaks.py
│   └── routes/
│
├── core/
│   ├── app.py
│   ├── images/
│   │   ├── emojis/
│   │   └── misc/
│   └── themes/
│       ├── blue_theme.json
│       └── green_theme.json
│
└── frontend/
    ├── styles.py
    ├── components/
    │   ├── glass_card.py
    │   ├── rounded_card.py
    │   └── screen_frame.py
    │
    ├── tabs/
    │   ├── goals_tab.py
    │   └── streaks_tab.py
    │
    └── widgets/
        ├── goal_row.py
        └── streak_row.py
```
## Notes

`life_manager.db` is used for local development data. In a production-ready version, this file would usually be ignored by Git and generated automatically.


## Setup

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment:

Windows:
```bash
.venv\Scripts\activate
```

Mac/Linux:
```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python main.py
```