Travis-CI Build Status auf dem Master: [![Build Status](https://travis-ci.org/PumucklOnTheAir/TestFramework.svg?branch=master)](https://travis-ci.org/PumucklOnTheAir/TestFramework.svg?branch=master)

Aufgaben:
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


### Ausführen
Über `python cli.py -h`können alle Subkommandos aufgelistet werden. 

`python cli.py status -h` listet alle optionalen Argumente für eine Statusübersicht auf

`python cli.py status -a` zeigt die Übersicht über alle Router an

`python cli.py status -r [Router ID]` zeigt detaillierte Infos zu einem bestimmten Router an (ID über status -a einsehbar)
     
     

_Konventionen, Vorgehensweise und Dokumentation im Wiki_

![Class Diagram](http://plantuml.com/plantuml/svg/3SSx3i8m303Ggy05ufsD4xG3UsLSAx68dSeVSNrusxkBqQoJo-TjP5xn073yjYuvwbt1JikIBHijXRsqw3CtUmr-YiFc7Kq2Sxa43GvGZ6G7cXXnbCxZ5EoEsgv_VW00?lol12)


