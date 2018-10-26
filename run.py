from app import create_app


app = create_app('development')

@app.route('/')
def index():
    return "<p><a href='https://documenter.getpostman.com/view/4074074/RWgxvFgE'>Documentation link</a></p>"

if __name__ == "__main__":
    app.run(debug=True)
