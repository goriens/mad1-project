from app import create_app

app=create_app()
if(__name__=="main"):
    app.run(debug=True)