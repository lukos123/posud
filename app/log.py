from datetime import datetime


def log(text, in_line=False, after_line=False):
    current_time = datetime.now()
    formatted_time = current_time.strftime("%y.%m.%d %H:%M:%S")
    end = "\n"
    if in_line:
        end = "\r"
    if after_line:
        print()
    print(formatted_time, text, end=end)

# def log_in_line(text):
#     current_time = datetime.now()
#     formatted_time = current_time.strftime("%y.%m.%d %H:%M:%S")

#     print(formatted_time, text, end='\r')
