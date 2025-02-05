from flask import Flask, render_template, jsonify
import subprocess

app = Flask(__name__)

# Function to run the Python script and get output
def run_python_script():
    try:
        result = subprocess.check_output(
            ["python", "script.py"], stderr=subprocess.STDOUT, text=True
        )
    except subprocess.CalledProcessError as e:
        result = e.output
    return result

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/run_python', methods=['GET'])
def run_python():
    output = run_python_script()
    return jsonify({"output": output})

if __name__ == "__main__":
    app.run(debug=True)
