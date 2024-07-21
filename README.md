## Prerequisites

- Python 3.9 or higher
Install python via conda or download from https://www.python.org/

## Installation

Follow these steps to install and set up the automatic clicker on Telegram:

1. **Clone the Repository**
   ```sh
   git clone https://github.com/DANDROZAVR/blum_farmer
   cd blum_farmer
   ```

2. **Create and Activate a Virtual Environment**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

## Setup

1. **Configure Telegram Accounts**
   - Ensure you have the phone numbers for each account that will be used to operate the clicker.
   - For the daily login part, it's highly suggests to use the corporate telegram's format. In a common folder, create folders starting from 0 (1, 2, ...), with each format as downloaded from here https://telegram.org/dl/desktop/win64_portable

2. **Edit the Configuration File**
   - Open the `config.json` file and edit the necessary parameters.
   - Example `config.json`:
     ```json
{
    "from_id": 0,
    "to_id": 5,
    "accounts_in_one_tg_profile": 3,

    "exe_path": "C:\\Users\\name\\Documents\\blum",
    "iterate_all_accs_times": 1,
    "SLOWMODE": 1,

    "play_account_id_from": "1_2",
    "play_account_id_to": "2_0",
    "do_tasks": true,
    "play_games": true,

    "api_key": 123123,
    "api_hash": "aaa"
}
     ```
   - **Note:** 
     - Replace the `api_key` and `api_hash` from https://my.telegram.org/apps (guide: https://docs.telethon.dev/en/stable/basic/signing-in.html#signing-in-as-a-bot-account)
     - `SLOWMODE` is how slow the script would work going through a daily check-in (by clicker)
     - `do_tasks` `play_games` is what you are gonna do with `3_play_game` (either tasks or game). `play_account_from` and `play_account_id_to` is the range of accounts you want to run the game/tasks for (simultaneously). Typically each game lasts about a minute, so better chill and wait. See below how to run it
     - `exe_path` is the path for a folder containing all your telegrams group (folders)
     - `MAX_GAME_WORKERS` is how many threads can play games at the same time (standard limit 5)
   
## Running the Script

1. **Create the sessions for telegram accounts**
   ```sh
   python 1_genereate_sessions.py
   ```

And look in terminal. For every account write a number two times, and then a code from telegram app

2. **Completing daily check-in and claiming farming(clicker)**
   ```sh
   python 2_main.py
   ```

3. **Completing daily check-in and claiming farming(clicker)**
   ```sh
   python 3_play_game.py
   ```

## Troubleshooting

- Ensure Python version 3.10 or higher is installed.
- Verify all dependencies are correctly installed.
- Double-check your phone numbers and ensure they are entered correctly.
- Verify the `config.json` file is correctly configured.

