from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import requests
from datetime import datetime
import google.generativeai as genai


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
genai.configure()


def configure_api_key(api_key):
  if not api_key:
    raise ValueError("Please provide your Gemini API key. Do not embed it in code!")
  genai.configure(api_key=api_key)

messages = []
test = {'hi':'hi, who are you?'}


@app.route('/premium')
def premium():
    return render_template('premium.html')

# Load JSON data from GitHub
def load_user_credentials():
    url = 'https://raw.githubusercontent.com/SivaVimel/LifeCareCharitableTrust/main/test.json'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Check if the entered credentials are valid
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    # Load user credentials from JSON
    user_credentials = load_user_credentials()
    
    if user_credentials and username in user_credentials:
        if user_credentials[username] == password:
            session['authenticated'] = True
            return jsonify({'success': True})
    
    return jsonify({'success': False, 'message': 'You are not an authenticated user.'})


@app.route('/')
def index():
    return render_template('index.html', messages=messages)

def replace_asterisks_with_strong_tags(message):
    result = []
    strong_tag_open = True
    i = 0
    
    while i < len(message):
        if message[i:i+2] == '**':
            if strong_tag_open:
                result.append('<strong>')
            else:
                result.append('</strong>')
            strong_tag_open = not strong_tag_open
            i += 2
        else:
            result.append(message[i])
            i += 1
    
    return ''.join(result)


@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        message = request.form['message']
        test['hi'] = message
        message = test['hi']
    except:
         message = test['hi']
    while True:
        # Gemini 1
        your_gemini_api_key = "AIzaSyC3aNlBGGmJqasAgBDEWXNe4aZgj4KyDCA"
        try:
          configure_api_key(your_gemini_api_key)
        except ValueError as e:
          print(f"Error: {e}")
          exit(1)

        model = genai.GenerativeModel('gemini-1.0-pro')
        response = model.generate_content(message)
        message = response.text
        message = replace_asterisks_with_strong_tags(message)
        message = message.replace('*','🔹')
        message = message.replace('.','<br>')
        name = 'Gemini 1.0: '
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        messages.append((name, message, timestamp))

        # Gemini 2
        your_gemini_api_key = "AIzaSyDWaRloPWy3JItGXrimp7hpeiZgl-OvJtQ"
        try:
          configure_api_key(your_gemini_api_key)
        except ValueError as e:
          print(f"Error: {e}")
          exit(1)

        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content(message)
        message = response.text
        message = replace_asterisks_with_strong_tags(message)
        message = message.replace('*','<br>🔹')
        message = message.replace('.','<br>')
        name = 'Gemini 1.5: '
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        messages.append((name, message, timestamp))
        test['hi'] = message
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
