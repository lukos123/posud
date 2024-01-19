from datetime import datetime


def log(text):
    current_time = datetime.now()
    formatted_time = current_time.strftime("%y.%m.%d %H:%M:%S")

    print(formatted_time, text)