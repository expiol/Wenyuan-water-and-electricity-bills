import requests
import sqlite3
from datetime import datetime
import threading
import time

# 添加请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# 指定代理
proxy = {
    'http': 'http://xxxxx.com:xxxxx',
    'https': 'http://xxxxx.com:xxxx'
}

# 并发请求线程数
num_threads = 5
# 每个线程隔多长时间切换代理IP， 建议15 - 60秒
session_alive = 15
# 请求失败后的重试次数
max_retries = 20
# 请求超时时间（秒）
request_timeout = 30

threads = []

def get_balance(user_sn, session):
    url = f'https://api.215123.cn/proxy/qy/sdcz/balance?buildingId=328001&userSn={user_sn}'
    for attempt in range(max_retries):
        try:
            response = session.get(url, headers=headers, proxies=proxy, timeout=request_timeout)
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    balance = float(data['message'])
                    if balance == 0.0:
                        return None  # 跳过余额为0.0的数据
                    return balance
                else:
                    print(f"Request for {user_sn} returned success=False")
                    return None
            elif response.status_code == 403:
                print(f"Request for {user_sn} returned status code 403 - Access denied. Waiting for retry...")
                time.sleep(15)  # 等待15秒以重试
            else:
                print(f"Request for {user_sn} returned status code {response.status_code}")
        except (requests.Timeout, requests.ConnectionError) as e:
            print(f"Request for {user_sn} timed out or connection error: {str(e)}. Retrying...")
            session.close()
            session = requests.Session()
        except requests.RequestException as e:
            print(f"RequestException occurred for {user_sn}: {str(e)}. Retrying...")
            session.close()
            session = requests.Session()
        except ValueError as e:
            print(f"ValueError occurred for {user_sn}: {str(e)}. Retrying...")
            session.close()
            session = requests.Session()

        # 等待一段时间后重试
        time.sleep(1 + attempt * 0.5)  # 每次重试增加等待时间
    return None

def save_balance(cursor, building, user_sn, balance):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    date = datetime.now().strftime('%Y-%m-%d')
    cursor.execute('SELECT COUNT(*) FROM balances WHERE user_sn = ? AND date = ?', (user_sn, date))
    count = cursor.fetchone()[0]
    if count == 0:
        cursor.execute('''
        INSERT INTO balances (building_id, user_sn, balance, timestamp, date) 
        VALUES (?, ?, ?, ?, ?)
        ''', (building, user_sn, balance, timestamp, date))
        cursor.connection.commit()  # 在每次插入数据后立即提交更改
        print(f"Inserted data for {user_sn} on {date}.")
    else:
        print(f"Data for {user_sn} on {date} already exists. Skipping...")

def process_building(building):
    floors = { '01': 23, '02': 23, '03': 23, '04': 23, '05': 26, '06': 26 }
    session = requests.Session()
    switch_time = time.time() + session_alive  # Set end time for session
    print(f"Processing building {building}...")

    # 创建数据库连接
    conn = sqlite3.connect('/root/wenyuan/balance_data.db')
    cursor = conn.cursor()

    for floor in range(2, floors[building] + 1):  # 从第二层开始
        print(f"  Processing floor {floor}...")
        for unit in range(1, 28):  # 每层楼有27个单元
            if time.time() > switch_time:
                session.close()
                session = requests.Session()
                switch_time = time.time() + session_alive  # Set end time for session
            user_sn = f'{building}-{floor:02d}{unit:02d}'
            balance = get_balance(user_sn, session)
            if balance is not None:
                save_balance(cursor, building, user_sn, balance)
            time.sleep(2)  # 延长请求之间的等待时间

    # 关闭数据库连接
    conn.close()
    print(f"Database connection closed for building {building}.")

def check_and_insert_missing_data():
    # 创建数据库连接
    conn = sqlite3.connect('/root/wenyuan/balance_data.db')
    cursor = conn.cursor()

    date = datetime.now().strftime('%Y-%m-%d')
    cursor.execute('SELECT user_sn FROM balances WHERE date = ?', (date,))
    existing_users = set(row[0] for row in cursor.fetchall())

    buildings = ['01', '02', '03', '04', '05', '06']
    floors = { '01': 23, '02': 23, '03': 23, '04': 23, '05': 26, '06': 26 }

    session = requests.Session()
    switch_time = time.time() + session_alive  # Set end time for session

    for building in buildings:
        for floor in range(2, floors[building] + 1):  # 从第二层开始
            for unit in range(1, 28):  # 每层楼有27个单元
                if time.time() > switch_time:
                    session.close()
                    session = requests.Session()
                    switch_time = time.time() + session_alive  # Set end time for session
                user_sn = f'{building}-{floor:02d}{unit:02d}'
                if user_sn not in existing_users:
                    balance = get_balance(user_sn, session)
                    if balance is not None:
                        save_balance(cursor, building, user_sn, balance)
                    time.sleep(2)  # 延长请求之间的等待时间

    # 关闭数据库连接
    conn.close()
    print("Checked and inserted missing data.")

def main():
    buildings = ['01', '02', '03', '04', '05', '06']
    start_time = time.time()

    for building in buildings:
        thread = threading.Thread(target=process_building, args=(building,))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    check_and_insert_missing_data()  # 检查并重新插入未插入的数据

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Execution time: {elapsed_time} seconds.")

if __name__ == '__main__':
    main()
