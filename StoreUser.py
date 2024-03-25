from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # Import CORS from flask_cors

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes in your Flask app

# Configure your database connection
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///E:\MenuOrderBarang\UserData.db'  # Example: SQLite database
db = SQLAlchemy(app)

# Define your database model
class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(100), nullable=False)
  password = db.Column(db.String(100), nullable=False)
  
@app.route('/api/checkUser', methods=['GET'])
def checkUser():
    try:
        username = request.args.get('username')
        user = User.query.filter_by(username=username).first()
        if user:
            return jsonify({'message': 'User exists'}), 404
        else:
            return jsonify({'message': 'User does not exist'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/login', methods=['GET'])
def login():
    try:
        username = request.args.get('username')
        password = request.args.get('password')

        # Check if the provided username and password match an existing user
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            return jsonify({'message': 'Login successful'}), 200
        else:
            return jsonify({'error': 'Invalid username or password'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Define your endpoint to handle form submissions
@app.route('/api/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # Create a new user instance
        new_user = User(username=username, password=password)
        # Add the user to the database session
        db.session.add(new_user)
        # Commit the changes to the database
        db.session.commit()

        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        # Rollback the changes if an error occurs
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)
