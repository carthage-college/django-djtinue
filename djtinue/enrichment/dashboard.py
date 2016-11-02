#app/dashboard.py
from grappelli.dashboard import Dashboard

class AdminDashboard(Dashboard):

    class Media:
        css = {
            'all': (
                '/static/djtinue/css/admin.css',
            )
        }
        #js = (
            #'js/mydashboard.js',
            #'js/myscript.js',
        #)
