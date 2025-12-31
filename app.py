from flask import Flask, render_template_string
import mysql.connector

app = Flask(__name__)

# ---------- MYSQL CONNECTION ----------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="enviro_db"
)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Smart Environment Monitoring</title>
    <meta http-equiv="refresh" content="5">
</head>
<body>

<h2>Last 50 Sensor Readings</h2>

<table border="1">
<tr>
    <th>Temperature (°C)</th>
    <th>Humidity (%)</th>
    <th>Gas</th>
    <th>Time</th>
</tr>

{% for row in rows %}
<tr>
    <td>{{ row.temperature }}</td>
    <td>{{ row.humidity }}</td>
    <td>{{ row.gas }}</td>
    <td>{{ row.time }}</td>
</tr>
{% endfor %}

</table>

</body>
</html>
"""

@app.route("/")
def index():
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT temperature, humidity, gas, time
        FROM sensor_data
        ORDER BY time DESC
        LIMIT 50
    """)
    rows = cursor.fetchall()
    cursor.close()
    return render_template_string(HTML, rows=rows)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
