from flask import Flask, render_template, request, redirect, url_for
import json
from urllib.parse import quote, unquote

app = Flask(__name__)

def calculate_bandwidth(clock_speed, channels):
    return (clock_speed * 2 * 64 * channels) / 8 / 1000

def calculate_latency(clock_speed, cas_latency):
    return (cas_latency / clock_speed) * 1000

@app.route('/', methods=['GET', 'POST'])
def index():
    data_string = request.args.get('data', '[]')
    user_results = json.loads(unquote(data_string))

    if request.method == 'POST':
        memory_name = request.form['memory_name']
        # --- Get the memory type from the form ---
        memory_type = request.form['memory_type'] 
        clock_speed = float(request.form['clock_speed'])
        channels = int(request.form['channels'])
        cas_latency = float(request.form['cas_latency'])

        bandwidth = calculate_bandwidth(clock_speed, channels)
        latency = calculate_latency(clock_speed, cas_latency)
        
        user_results.append({
            "name": memory_name,
            # --- Save the memory type in the results ---
            "memory_type": memory_type, 
            "bandwidth": round(bandwidth, 2),
            "latency": round(latency, 2)
        })
        
        new_data_string = quote(json.dumps(user_results))
        return redirect(url_for('index', data=new_data_string))

    return render_template('index.html', user_results=user_results)

@app.route('/clear')
def clear_results():
    return redirect(url_for('index'))

# This part is only for local testing, Gunicorn runs the app in production
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)