from app import create_app


app = create_app('development')

@app.route('/')
def index():
    return "<p> Documentation link: https://documenter.getpostman.com/view/4074074/RWgxvFgE</p>"

if __name__ == "__main__":
    app.run(debug=True)
