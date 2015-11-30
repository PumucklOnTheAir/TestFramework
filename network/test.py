#sys.path.append('/root/TestFramework/network')
#sys.path.append('/home/simon/TestFramework/network/')
#sys.path.append('/home/pi/TestFramework/network/')
from Router.router import Router
from util.router_info import  Router_info

from network_ctrl import Network_Ctrl

routers = Router.get_manual_configured_routers()
Router_info.load(routers)
#network_ctrl = Network_Ctrl(routers[0])
#network_ctrl.connect_with_router()
#network_ctrl.configure_router()
routers[0].print_infos()
#network_ctrl.exit()