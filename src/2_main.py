import json
import subprocess
import time
import logging

from src.clicker import Clicker

# Load configuration
def load_config(config_path='config/config.json'):
    global SLOWMODE
    with open(config_path, 'r') as file:
        config = json.load(file)
    SLOWMODE = config["SLOWMODE"]
    return config['from_id'], config['to_id'], config['exe_path'], config


# Placeholder for user-defined operations using Clicker class
def perform_daily_checking(clicker):
    clicker.click(940, 600)
    time.sleep(2)
    clicker.click(900, 850)
    time.sleep(0.55)
    clicker.click(950, 750)
    time.sleep(3 * min(1., SLOWMODE / 2))
    clicker.click(950, 750)
    time.sleep(0.75)
    clicker.click(950, 750)
    time.sleep(0.1)

def perform_entering_blum_app(clicker):
    clicker.click(150, 55)
    time.sleep(0.2 * min(1., SLOWMODE / 2))
    clicker.write("@BlumCryptoBot")
    time.sleep(2)
    clicker.click(150, 155)
    time.sleep(0.4 * min(1., SLOWMODE / 2))
    clicker.click(1000, 1000)
    time.sleep(0.2 * min(1., SLOWMODE / 2))
    clicker.write("/start")
    clicker.enter()
    time.sleep(0.5 * min(1., SLOWMODE / 2))
    clicker.click(1000, 888)
    time.sleep(0.5 * min(1., SLOWMODE / 2))

def perform_swtiching_profile_in_group(clicker, acc):
    clicker.click(20, 40)
    time.sleep(0.25 * min(1., SLOWMODE / 2))
    clicker.click(30, 230 + acc * 50)

def perform_closing_app(clicker):
    clicker.click(1150, 100)
    time.sleep(0.3 * min(1., SLOWMODE / 2))

def perform_closing_telegram(clicker):
    clicker.click(1900, 10)
    time.sleep(0.3 * min(1., SLOWMODE / 2))

# Main script function
def main():
    from_id, to_id, exe_path, config = load_config()
    clicker = Clicker()

    times = config["iterate_all_accs_times"]
    print(f'iterating {times} times')
    for i in range(0, times):
        print(i)
        print(i)
        print(i)
        # only_collect_blum = True
        only_collect_blum = False
        if only_collect_blum:
            active_blum_apps = 15
            from_id = 10000000000
            time.sleep(10)
        else:
            active_blum_apps = 0

        for id in range(from_id, to_id + 1):
            print(f"Running process for ID: {id}")
            logging.info(f"Starting process for ID: {id}")
            print('DO NOT TOUCH ANYTHING')
            print('DO NOT TOUCH ANYTHING')
            print('DO NOT TOUCH ANYTHING')
            print('DO NOT TOUCH ANYTHING')
            print('DO NOT TOUCH ANYTHING')
            # Run the executable (simulate this part for now)
            proc = subprocess.Popen([exe_path + '/' + str(id) + "/Telegram.exe"])

            print()
            time.sleep(10 * SLOWMODE)

            for acc in range(0, config["accounts_in_one_tg_profile"]): # 3 accs in a group
                # switching to another account inside group
                perform_swtiching_profile_in_group(clicker, acc)
                time.sleep(0.5 * min(1., SLOWMODE / 2.5))
                print(acc)

                perform_entering_blum_app(clicker)
                time.sleep(0.35 * SLOWMODE)
                active_blum_apps += 1
            time.sleep(0.5)
            perform_closing_telegram(clicker)

        time.sleep(15)
        for i in range(0, active_blum_apps):
            time.sleep(5 * min(1., SLOWMODE / 2))
            perform_daily_checking(clicker)  # claim farming
            time.sleep(5 * SLOWMODE)
            perform_daily_checking(clicker)  # start farming
            time.sleep(0.5 * SLOWMODE)
            perform_closing_app(clicker)

if __name__ == "__main__":
    main()
