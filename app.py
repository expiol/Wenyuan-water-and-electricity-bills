from flask import Flask, request, render_template
import sqlite3
from datetime import datetime

app = Flask(__name__)

def normalize_building(building):
    # 去除所有非数字字符，然后转化为两位数字形式
    building = ''.join(filter(str.isdigit, building))
    return f'{int(building):02d}'

def format_building(building):
    return f'D{building}'

def query_balance(building, unit_number):
    conn = sqlite3.connect('balance_data.db')
    cursor = conn.cursor()
    
    # 规范化楼号和门牌号
    building_normalized = normalize_building(building)
    unit_number = f'{int(unit_number):04d}'
    user_sn = f'{building_normalized}-{unit_number}'
    start_date = '2024-07-06'
    end_date = datetime.now().strftime('%Y-%m-%d')
    
    cursor.execute('''
    SELECT date, balance FROM balances
    WHERE user_sn = ?
    AND date BETWEEN ? AND ?
    ORDER BY date DESC
    LIMIT 10
    ''', (user_sn, start_date, end_date))
    
    rows = cursor.fetchall()
    conn.close()
    
    # 将结果反转，使最近的记录显示在最前面
    rows.reverse()
    
    return rows, building_normalized

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        building = request.form.get('building')
        unit_number = request.form.get('unit_number')
        
        if not building or not unit_number:
            return render_template('index.html', error="请填写所有字段", results=None)
        
        try:
            results, building_normalized = query_balance(building, unit_number)
            building_formatted = format_building(building_normalized)
        except ValueError:
            return render_template('index.html', error="楼号和门牌号必须是数字", results=None)
        
        return render_template('index.html', results=results, building=building_formatted, unit_number=unit_number)
    
    return render_template('index.html', results=None, building=None, unit_number=None)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
