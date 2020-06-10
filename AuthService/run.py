from app import app
app.env="development"
app.run(host='localhost', port=5000 , debug=True)