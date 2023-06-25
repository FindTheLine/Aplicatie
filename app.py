from website import create_app

ENV = 'dev'

app = create_app(ENV) 

if __name__ == '__main__':
    if ENV == "dev":
        app.run(debug=True)
    if ENV == "prod":
        app.run(debug=False)
        