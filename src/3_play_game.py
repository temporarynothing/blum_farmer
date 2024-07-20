import concurrent

import numpy as np
import time
import requests
import time
import urllib

from src.cache_data import SimpleCache

access_token = ''
last_refresh_time = time.time()
blum_base = "https://game-domain.blum.codes/api/v1/"
url_play = f"{blum_base}game/play"
url_claim = f"{blum_base}game/claim"
url_balance = f"{blum_base}user/balance"
url_tasks = f"{blum_base}tasks"
url_refresh = "https://gateway.blum.codes/v1/auth/refresh"
generate_refresh_and_access_token = 'https://gateway.blum.codes/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP'

standard_headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "priority": "u=1, i",
    "sec-ch-ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Microsoft Edge\";v=\"126\", \"Microsoft Edge WebView2\";v=\"126\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site"
}
post_headers = standard_headers
post_headers.update({"content-type": "application/json"})

MIN_AMOUNT_POINTS = 140
MAX_AMOUNT_POINTS = 240


def extract_auth_data(url: str) -> str:
    return urllib.parse.unquote(url).split('tgWebAppData=')[1].split('&tgWebAppVersion')[0]

def provider_telegram_mini_app(url):
    authDate = extract_auth_data(url)

    data = {'query': authDate}

    response = requests.post('https://gateway.blum.codes/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP', json=data).json()
    refresh = response['token']['refresh']
    access = response['token']['access']
    return refresh, access

def do_refresh_token(account_id):
    global access_token, last_refresh_time
    last_refresh_time = time.time()
    accounts = SimpleCache("accounts")
    if accounts.exists(account_id):
        refresh_token = accounts.get(account_id)["refresh_token"]
    else:
        refresh_token = None

    need_update_refresh = False
    if refresh_token:
        response_claim = requests.post(url_refresh, headers=post_headers, json={"refresh": refresh_token})

        if response_claim.status_code != 200:
            need_update_refresh = True
        print(response_claim.status_code)
        print(response_claim.json())
    else:
        need_update_refresh = True


    if need_update_refresh:
        cache_urls = SimpleCache(account_id)
        url = cache_urls.get("blum_url")
        refresh_token, access_token = provider_telegram_mini_app(url)
    else:
        access_token = response_claim.json()["access"]
        refresh_token = response_claim.json()["refresh"]

    standard_headers.update({"authorization": f"Bearer {access_token}"})
    post_headers.update({"authorization": f"Bearer {access_token}"})

    accounts.set("refresh_token", refresh_token)
    accounts.set("access_token", access_token)

def get_balance_tickets():
    response_play = requests.get(url_balance, headers=standard_headers)
    print(response_play.status_code)
    print(response_play.json())
    tickets_number = response_play.json()["playPasses"]
    return tickets_number


def run_game():
    response_play = requests.post(url_play, headers=standard_headers)
    print(response_play.status_code)
    print(response_play.json())
    gameId = response_play.json()["gameId"]
    # gameid = "eb0efac1-0cdf-4d0e-bc17-cbe61fe2e527"
    return gameId

def claim_game_reward(gameId: str):
    value = np.random.randint(MIN_AMOUNT_POINTS, MAX_AMOUNT_POINTS)
    if np.random.randint(0, 20) == 5:  # 1 of 20 tries
        value = np.random.randint(1, 40)
        print('simulating bomb! would receive much more less than usual')
    print(f'would win that amount of blum points: {value}')

    payload_claim = {
        "gameId": gameId,
        "points": value
    }
    response_claim = requests.post(url_claim, headers=post_headers, json=payload_claim)
    print(response_claim.status_code)

def get_tasks_list():
    response_tasks_list = requests.get(url_tasks, headers=standard_headers)
    print(response_tasks_list.status_code)
    return response_tasks_list.json()

def start_task(task_id: str):
    response_start_task = requests.post(url_tasks + "/" + task_id + "/start", headers=standard_headers)
    print(response_start_task.status_code)

def claim_task(task_id: str):
    response_claim_task = requests.post(url_tasks + "/" + task_id + "/claim", headers=standard_headers)
    print(response_claim_task.status_code)

def _make_available_actions_on_tasks(all_tasks):
    for task in all_tasks:
        if task["type"] == "PROGRESS_TARGET" and task["status"] == "NOT_STARTED":
            continue
        if task["status"] == "NOT_STARTED":
            start_task(task["id"])
            sleep(1)
        elif task["status"] == "READY_FOR_CLAIM":
            claim_task(task["id"])
            sleep(1)

def try_complete_all_tasks():
    print('completing tasks')
    _make_available_actions_on_tasks(get_tasks_list())
    print('waiting for tasks beeing completed')
    sleep(60)
    _make_available_actions_on_tasks(get_tasks_list())
    sleep(5)
    print('tasks completed!')

def play_all_possible_games(play_account_id):
    available_tickets = get_balance_tickets()
    for ticket in range(available_tickets):
        if (time.time() - last_refresh_time > 55 * 60):
            do_refresh_token(play_account_id)
        gameId = run_game()
        sleep(np.random.randint(30, 55))  # simulating waiting between start and end of the game
        claim_game_reward(gameId)
        sleep(np.random.randint(3, 75))

def sleep(sec: int):
    print(f'going to sleep for {sec} seconds')
    time.sleep(sec)

def chill_and_play(play_account_id):
    if "_" not in str(play_account_id):
        play_account_id = str(play_account_id / accounts_in_one_tg_profile) + "_" + str(play_account_id % accounts_in_one_tg_profile)
    do_refresh_token(play_account_id)

    if global_config.get("do_tasks"):
        try_complete_all_tasks()
    if global_config.get("play_games"):
        play_all_possible_games(play_account_id)


if __name__ == "__main__":
    global_config = SimpleCache("config")
    play_account_id_from = global_config.get("play_account_id_from")
    play_account_id_to = global_config.get("play_account_id_to")
    limit_group = global_config.get("accounts_in_one_tg_profile")
    MAX_GAME_WORKERS = global_config.get("MAX_GAME_WORKERS")
    f_group, f_acc = play_account_id_from.split("_")
    s_group, s_acc = play_account_id_to.split("_")

    accounts = [f"{group}_{acc}" for group in range(int(f_group) + 1, int(s_group)) for acc in range(0, int(limit_group))]
    accounts.extend(f"{f_group}_{acc}" for acc in range(int(f_acc), limit_group))
    accounts.extend(f"{s_group}_{acc}" for acc in range(0, int(s_acc) + 1))

    accounts_in_one_tg_profile = global_config.get("accounts_in_one_tg_profile")

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_GAME_WORKERS) as executor:
        # Map the hello_world function to the list of IDs
        results = executor.map(chill_and_play, accounts)

    # OR COMPLETE TASKS
    pass