from flask import Flask
from app.routes import main_bp
import os

def create_app():
    app = Flask(__name__, 
                static_folder='static',
                template_folder='templates')
    
    # Register blueprints
    app.register_blueprint(main_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)