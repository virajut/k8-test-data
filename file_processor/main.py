from src import create_app,db

if __name__ == "__main__":
    app = create_app()
    db=db
    print(db)
    app.run(debug=True, host="0.0.0.0", port="5000")  # nosec
