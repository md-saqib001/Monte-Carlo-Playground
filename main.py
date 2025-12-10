from website import create_app

app = create_app()

if __name__ == '__main__':
    # debug=True means the server auto-reloads when you change code
    # It also provides a debugger in the browser if code crashes
    app.run(debug=True)