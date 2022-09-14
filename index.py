from website import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=False)

# Commands to get server running:
# pip3 freeze > requirements.txt
