wsgi_app = "mealwise.wsgi:application"
loglevel = "debug"
workers = 2
bind = "0.0.0.0:8000"
reload = True
accesslog = errorlog = "/home/ubuntu/log/mealwise.log"
capture_output = True
pidfile = "/home/ubuntu/run/mealwise.pid"
