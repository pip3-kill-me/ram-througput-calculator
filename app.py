from flask import Flask, render_template, request

app = Flask(__name__)

def calculate_bandwidth(clock_speed, bus_width, channels):
    return clock_speed * bus_width * channels * 8 / 1_000_000_000  # GB/s

def calculate_latency(clock_speed, cas_latency):
    return cas_latency / clock_speed * 1000  # ns

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        clock_speed = float(request.form['clock_speed'])
        bus_width = int(request.form['bus_width'])
        channels = int(request.form['channels'])
        cas_latency = float(request.form['cas_latency'])

        bandwidth = calculate_bandwidth(clock_speed, bus_width, channels)
        latency = calculate_latency(clock_speed, cas_latency)

        return render_template('index.html', bandwidth=bandwidth, latency=latency)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
