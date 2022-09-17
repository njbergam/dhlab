from flaskr.__init__ import create_app

app = create_app()

csp = {
    'default-src': [
        '\'self\'',
        '\'unsafe-inline\'',
        'stackpath.bootstrapcdn.com',
        'code.jquery.com',
        'cdn.jsdelivr.net'
    ]
}


if __name__ == "__main__":
    app.run()
