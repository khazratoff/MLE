from .app import app


def main():
    print(
        "* Loading Keras model and Flask starting server... please wait until server has fully started"
    )
    app.run(host="0.0.0.0")
