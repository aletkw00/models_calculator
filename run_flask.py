from flaskr import app, db

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True)
else:
    # Creates the database and tables 
    # for the production environment    
    with app.app_context():
        db.create_all()