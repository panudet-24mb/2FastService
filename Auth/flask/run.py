from app import app
app.env="development"
app.run(host='0.0.0.0', port=5000 ,threaded=True, debug=True)