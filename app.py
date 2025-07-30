from flask import Flask, render_template, request, redirect, url_for
import json
from urllib.parse import quote, unquote

app = Flask(__name__)

# No secret key is needed because we are not using sessions.

def calculate_bandwidth(clock_speed, channels):
    return (clock_speed * 2 * 64 * channels) / 8 / 1000

def calculate_latency(clock_speed, cas_latency):
    return (cas_latency / clock_speed) * 1000

@app.route('/', methods=['GET', 'POST'])
def index():
    # On a GET request, get the data from the URL query string.
    # If it doesn't exist, start with an empty list.
    data_string = request.args.get('data', '[]')
    user_results = json.loads(unquote(data_string))

    if request.method == 'POST':
        # Get new data from the form
        memory_name = request.form['memory_name']
        clock_speed = float(request.form['clock_speed'])
        channels = int(request.form['channels'])
        cas_latency = float(request.form['cas_latency'])

        # Calculate results
        bandwidth = calculate_bandwidth(clock_speed, channels)
        latency = calculate_latency(clock_speed, cas_latency)
        
        # Add the new result to our current list of results
        user_results.append({
            "name": memory_name,
            "bandwidth": round(bandwidth, 2),
            "latency": round(latency, 2)
        })
        
        # Convert the entire list to a JSON string, URL-encode it,
        # and redirect back to the index with the data in the URL.
        new_data_string = quote(json.dumps(user_results))
        return redirect(url_for('index', data=new_data_string))

    # For the initial GET or after a redirect, render the page
    # with the data we parsed from the URL.
    return render_template('index.html', user_results=user_results)

@app.route('/clear')
def clear_results():
    # To clear, just redirect to the index with no data.
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)