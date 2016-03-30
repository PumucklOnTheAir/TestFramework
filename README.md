[![Build Status](https://travis-ci.org/PumucklOnTheAir/TestFramework.svg?branch=master)](https://travis-ci.org/PumucklOnTheAir/TestFramework)[![Documentation Status](https://readthedocs.org/projects/freifunk-testframework/badge/?version=master)](http://freifunk-testframework.readthedocs.org/en/master/?badge=master)[![codecov.io](https://codecov.io/github/PumucklOnTheAir/TestFramework/coverage.svg?branch=master)](https://codecov.io/github/PumucklOnTheAir/TestFramework?branch=master)[![Code Climate](https://codeclimate.com/github/PumucklOnTheAir/TestFramework/badges/gpa.svg)](https://codeclimate.com/github/PumucklOnTheAir/TestFramework)[![Issue Count](https://codeclimate.com/github/PumucklOnTheAir/TestFramework/badges/issue_count.svg)](https://codeclimate.com/github/PumucklOnTheAir/TestFramework)

Issues:
[![Stories in Ready](https://badge.waffle.io/PumucklOnTheAir/TestFramework.svg?label=ready&title=Ready)](http://waffle.io/PumucklOnTheAir/TestFramework)
[![Stories in Ready](https://badge.waffle.io/PumucklOnTheAir/TestFramework.svg?label=In%20Progress&title=In%20Progress)](http://waffle.io/PumucklOnTheAir/TestFramework)
[![Stories in Ready](https://badge.waffle.io/PumucklOnTheAir/TestFramework.svg?label=review&title=Review)](http://waffle.io/PumucklOnTheAir/TestFramework)
# FreifunkTestFramework

Die Dokumentation befindet sich online auf https://freifunk-testframework.readthedocs.org

Git Cheat Sheet http://www.git-tower.com/blog/git-cheat-sheet/

Tickets und Aufgabenplanung auf
https://waffle.io/PumucklOnTheAir/TestFramework/

## Bedienung

### Starten
Server manuel starten mit `python3 start_server.py` oder `./start_server.py`

Wen das FreifunkTestFramework schon als Service installiert ist, dann kann man über systemd es starten:
`systemctl start fftserver`


### Installieren
Die Installation ist ziemlich einfach unter einem Unix-System.
Ein `./install.sh` bzw. `sh install.sh` unter root reicht aus.
Es wird systemd und Python 3.4+ vorausgesetzt. Installation wurde lediglich unter Raspbian getestet.

Alternativ wen man den Testserver nur ausführen aber nicht als Service installiert haben möchte, kann man auch nur die Bibliothek installieren: `pip3 install -r requirements.txt`

### Testen
Eine Auswahl an Unittest fürs Framwork wird bei jedem Pull-Request auf Travis CI ausgeführt.
Eine vollständiges Testens des Frameworks ist auf dem Raspberry Pi möglich mit folgendem Kommando im Repo Ordner:
python3 -m unittest discover -s framework_unittests

### Ausführen
Command-List:

status		[-r/--router ID]:
	Shows a table. For each router it displays:
	ID, MODEL/Version, VLAN_ID, MODE, IP, MAC.
	With the flags "-r" and the Router_ID more informations about the given router
	are shown: ID, MODEL, MAC, IP, VLAN-NAME, VLAN-ID, MODE, USER_NAME, USER_PWD,
	POWERSOCKET_ID, NODE_NAME, PUBLIC_KEY, MEMORY_INFOS, NETWORK_INTERFACES,
	CPU_PROCESSES, SOCKET, MESH_CONNECTIONS.

sysupdate       [-r/--routers ID ID...]:
	Downloads FreiFunk-Firmware(s) onto the Host-System(RaspberryPI).
	With the flag "-r" and the Router_ID the matching Firmware-Image of a router
	will be downloaded. Without the flag for all the routers the Firmware-Images
	will be downloaded. It's also possible to download all Firmware-Images onto
	the Host-System, therefore the flag "DOWNLOAD_ALL" in the Config-File
	has to be "True". Before a firmware is downloaded the Framework checks,
	if the firmware already exists on the Host-System. If so the firmware is only
	imported into the framework. After the download of a Firmware-Image the Hash
	will be proved. In case of a failure three further attempts have been made.

sysupgrade      [-r/--routers ID ID... | -n/--n]:
	Upgrades the routers. With the flag "-r" and the Router_ID only the given
	router will be downloading the Firmware-Image from the Host-System.
	Then the sysupgrade	will be carried out and the router will be rebooted.
	The flag "-n" rejects the last firmware configurations.
	Info:
		- The systemupgrade will cause a TimeoutError, because network-ctrl waits
		for a ssh-response the is never returned. After this TimeoutError the
		router should have rebooted and response to the dhclient.
		- If no IP is returned by the dhcient, try the online-command, because
		it may take some time till the router is ready.

reboot          [-r/--routers ID ID... | -c/--config]:
	Reboots the routers. With the flag "-r" and the Router_ID only the given
	router will be rebooted.
	With the flag "-c" the router will be rebooted into the Config-Mode.
	Info:
		- If no IP is returned by the dhcient, try the online-command, because
		it may take some time till the router is ready.

webconfig       [-r/--routers ID ID... | -w/--wizard]:
	Configures the WebInterface of the routers. With the flag "-r" and
	the Router_ID only the given router will be configured. With the flag "-w" the
	wizard-page will be configured and the router also rebooted into Normal-Mode.
	Before the reboot, the public-key of the router has been parsed and stored.
	Without the flag "-w", the configurations of the expert-pages will be set.
	Info:
	 	- If no IP is returned by the dhcient, try the online-command, because
		it may take some time till the router is ready.

update     	[-r/--routers ID ID...]:
	Downloads information of the routers. With the flag "-r" and
	the Router_ID only the informations of the given router will be downloaded:
	ID, MODEL, MAC, IP, VLAN-NAME, VLAN-ID, MODE, USER_NAME, USER_PWD,
	POWERSOCKET_ID, NODE_NAME, PUBLIC_KEY, MEMORY_INFOS, NETWORK_INTERFACES,
	CPU_PROCESSES, SOCKET, UCI-KEYS/VALUES, MESH_CONNECTIONS.

online          [-r/--routers ID ID...]:
	Set the router-objects into the right modes. With the flag "-r" and
	the Router_ID only the given router is used. The online-command expect
	an IP via the dhclient and tries to ping the router on the matching mode.
	Info:
		- If no IP is returned by the dhcient, try the online-command again, because
		it may take some time till the router is ready.

power           [-r/--routers ID ID... | --on | --off]:
	Turns the power of the routers "on" or "off". If the flag is "--off" the router
	is set into off-mode. If the flag is set "--on" the router is set into normal-mode.
	Info:
	 	- If no IP is returned by the dhcient, try the online-command, because
		it may take some time till the router is ready.

start           [-r/--routers ID ID... | -s/--set NAME | -b/--blocking]:
	Executes firmware-tests on the routers. With the flag "-r" and
	the Router_ID the tests are only executed on the given router. The tests that are
	executed are all in the same Test-Set and this has to bee given with the flag "-s"
	and the Set_Name. With the flag "-b" the CLI is only released
	after the tests are finished.The results can be viewed with the results-command.

results         [-r/--routers ID ID... | -d/--delete | -f/--failure INDEX | -e/--errors INDEX]:
	Shows the results of the executed firmware-tests. With the flag "-r" and
	the Router_ID only the tests of the given router are shown:
	TEST_ID, ROUTER_ID, TEST_NAME, RESULT. If a failure or an error occur, the flags
	"-f" and "-e" can be used with the Test_ID to view the trace-back. The results
	will be stored persistent and imported during the start of the server. The flag
	"-d" deletes all results.

register    	[-r/--routers ID ID...]:
	Register the public-key of the routers. With the flag "-r" and
	the Router_ID only the public-key of the given router will be registered. This
	means that the public-key will be send to an email-address that is written in
	the Config-File. This is only possible if a webconfig-command with flag "-w"
	as been executed, so the public-key is available.

sets       	[-s/--set NAME]:
	Shows all Test-Sets that are available, with: TEST_SET_NAME, FIRMWARE_TESTS.
	Without the flag "-s" only four tests are shown per Test-Set. With the flag "-s"
	and a TEST_SET_ID all tests of a Test-Set are shown.

jobs      	[-r/--router ID]:
	Shows all jobs and tests that are currently running or waiting.
	With the flag "-r" and the Router_ID only the jobs and tests of the given router
	are shown.

