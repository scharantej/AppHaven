 
# Import necessary libraries
from flask import Flask, render_template, request, jsonify
import sqlite3

# Create a Flask app
app = Flask(__name__)

# Database connection
conn = sqlite3.connect('apk_store.db')
c = conn.cursor()

# Routes
@app.route('/')
def index():
    # Fetch all apps from the database
    c.execute('SELECT * FROM apps')
    apps = c.fetchall()

    # Render the index page with the list of apps
    return render_template('index.html', apps=apps)

@app.route('/app/<app_id>')
def app_detail(app_id):
    # Fetch the app details from the database
    c.execute('SELECT * FROM apps WHERE app_id=?', (app_id,))
    app = c.fetchone()

    # Render the app detail page
    return render_template('app_detail.html', app=app)

@app.route('/developer/dashboard')
def developer_dashboard():
    # Fetch all apps of the current developer
    developer_id = 1  # Assuming the current developer has ID 1
    c.execute('SELECT * FROM apps WHERE developer_id=?', (developer_id,))
    apps = c.fetchall()

    # Render the developer dashboard
    return render_template('developer_dashboard.html', apps=apps)

@app.route('/api/apps')
def api_apps():
    # Fetch all apps from the database
    c.execute('SELECT * FROM apps')
    apps = c.fetchall()

    # Convert the apps to JSON format
    json_apps = jsonify(apps)

    # Return the JSON response
    return json_apps

@app.route('/api/apps/<app_id>')
def api_app_detail(app_id):
    # Fetch the app details from the database
    c.execute('SELECT * FROM apps WHERE app_id=?', (app_id,))
    app = c.fetchone()

    # Convert the app to JSON format
    json_app = jsonify(app)

    # Return the JSON response
    return json_app

@app.route('/api/apps/upload', methods=['POST'])
def api_app_upload():
    # Get the app details from the request
    app_name = request.form['app_name']
    app_description = request.form['app_description']
    app_icon = request.files['app_icon']
    app_file = request.files['app_file']

    # Save the app details to the database
    c.execute('INSERT INTO apps (app_name, app_description, app_icon, app_file, developer_id) VALUES (?, ?, ?, ?, ?)',
              (app_name, app_description, app_icon.read(), app_file.read(), 1))  # Assuming the current developer has ID 1
    conn.commit()

    # Return a success message
    return jsonify({'success': True})

@app.route('/api/apps/<app_id>/update', methods=['POST'])
def api_app_update(app_id):
    # Get the app details from the request
    app_name = request.form['app_name']
    app_description = request.form['app_description']
    app_icon = request.files['app_icon']
    app_file = request.files['app_file']

    # Update the app details in the database
    c.execute('UPDATE apps SET app_name=?, app_description=?, app_icon=?, app_file=? WHERE app_id=?',
              (app_name, app_description, app_icon.read(), app_file.read(), app_id))
    conn.commit()

    # Return a success message
    return jsonify({'success': True})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
