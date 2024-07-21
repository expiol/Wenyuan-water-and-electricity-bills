# Wenyuan Water and Electricity Bills

This project includes web pages built with Flask and web crawlers written in Python.

## Project Description

The purpose of this project is to manage and track water and electricity bills for Wenyuan buildings. The web interface allows users to input building and room numbers to check their balances, schedule daily balance checks, save balances to a database, and visualize daily balance changes.

## Features

- Input building and room numbers to check balances.
- Schedule daily balance checks at 9 AM.
- Save balances to a database.
- Visualize daily balance changes from the schedule's start date.

## Using Proxies to Bypass Anti-Scraping Mechanisms

Due to anti-scraping mechanisms, it is necessary to switch proxies to retrieve data. Below is the code snippet to specify proxies:

```python
proxy = {
    'http': 'http://xxxxx.com:xxxxx',
    'https': 'http://xxxxx.com:xxxx'
}
```

## Installation

1. Clone the repository:
    
    ```bash
    git clone https://github.com/expiol/Wenyuan-water-and-electricity-bills.git
    cd Wenyuan-water-and-electricity-bills
    ```
    

## Usage

1. Run the Flask application to start the website:
    
    ```bash
    nohup python3 app.py &
    ```
    
2. Run the web crawler to fetch data:
    
    ```bash
    nohup python3 get_balance.py &
    ```
    
3. Open your web browser and navigate to `http://localhost:5000`.
    

## Setting Up a Scheduled Task

You can add a cron job to automatically run the crawler script at scheduled intervals to ensure the data is updated regularly. Here is how you can add a cron job to run `get_balance.py` every day at 9 AM:

1. Open the crontab file:
    
    ```bash
    crontab -e
    ```
    
2. Add the following line to the crontab file to schedule the task:
    
    ```bash
    0 9 * * * /usr/bin/python3 /path/to/your/Wenyuan-water-and-electricity-bills/get_balance.py >> /path/to/your/Wenyuan-water-and-electricity-bills/logs/get_balance.log 2>&1
    ```
    
    Replace `/usr/bin/python3` with the path to your Python 3 executable, and `/path/to/your/Wenyuan-water-and-electricity-bills` with the path to your project directory.
    

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.

```
