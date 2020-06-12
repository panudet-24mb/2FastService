from app import app
app.env="development"
# app.run( port=5001 , threaded=True, debug=True)

app.run(host='0.0.0.0', port=5001 ,threaded=True,  debug=True)