from app import create_app

# Create an instance of the app to be used by Gunicorn
app = create_app()

if __name__ == '__main__':
    app.run()
