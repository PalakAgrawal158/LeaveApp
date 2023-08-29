from apscheduler.schedulers.background import BackgroundScheduler


def display():
    print("Hi")

scheduler = BackgroundScheduler()
scheduler.add_job(display, 'interval', seconds = 5)

scheduler.start()