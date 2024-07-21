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
