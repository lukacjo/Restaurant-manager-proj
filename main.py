from website import create_app
# main appka z której odpalam całego flaska
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port="8047") # rónie jest z portami wiec akurat ten ale mona jakikolwiek wolny wybrać