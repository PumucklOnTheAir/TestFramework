from threading import Thread
from network.network_ctrl import Network_Ctrl

class Router_info:
    @staticmethod
    def load(routers):
        '''
        : Desc : starts a thread for each router and stores new information
        :param routers: list of router objects
        :return:
        '''
        for router in routers:
            worker = Worker(router)
            worker.start()
            router = worker.join()

class Worker(Thread):
    def __init__(self, router):
        Thread.__init__(self)
        self.router = router
        self.daemon = True

    def run(self):
        '''
        : Desc : runs new thread and gets the information from the router via ssh
        :return:
        '''
        print("run new thread ...")
        self.network_ctrl = Network_Ctrl(self.router)
        self.network_ctrl.connect_with_router()
        #Model
        self.router.model = self.network_ctrl.send_router_command('cat /proc/cpuinfo | grep machine').split(":")[1][:-4]
        #MAC
        self.router.mac = self.network_ctrl.send_router_command('uci show network.client.macaddr').split('=')[1][:-4]
        #SSID
        self.router.ssid = self.network_ctrl.send_router_command('uci show wireless.client_radio0.ssid').split('=')[1][:-4]
        self.network_ctrl.exit()

    def join(self):
        Thread.join(self)
        return self.router