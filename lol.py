from server.server import Server
from DaemonLite import DaemonLite

class Staff(DaemonLite) :
    def run(self):
        Server.start()



if __name__ == "__main__":
    # execute only if run as a script
    staff = Staff('staff.pid')
    staff.start()

