Build status auf dem Master: [![Build Status](https://travis-ci.org/PumucklOnTheAir/TestFramework.svg?branch=master)](https://travis-ci.org/PumucklOnTheAir/TestFramework.svg?branch=master)

Tasks:
[![Stories in Ready](https://badge.waffle.io/PumucklOnTheAir/TestFramework.svg?label=ready&title=Ready)](http://waffle.io/PumucklOnTheAir/TestFramework)
[![Stories in Ready](https://badge.waffle.io/PumucklOnTheAir/TestFramework.svg?label=In%20Progress&title=In%20Progress)](http://waffle.io/PumucklOnTheAir/TestFramework)
[![Stories in Ready](https://badge.waffle.io/PumucklOnTheAir/TestFramework.svg?label=review&title=Review)](http://waffle.io/PumucklOnTheAir/TestFramework)
# FreifunkTestFramework

Git Cheat Sheet http://www.git-tower.com/blog/git-cheat-sheet/

## Bedienung

### Starten
Server manuel starten mit `python3 start_server.py` oder `./start_server.py`

Wenn das FreifunkTestFramework schon als Service installiert ist, dann kann man über systemd es starten:
`systemctl start fftserver`

Tickets und Aufgabenplanung auf
https://waffle.io/PumucklOnTheAir/TestFramework/

Organisatorisches auf 
https://waffle.io/PumucklOnTheAir/Organisatorisches/

### Installieren
`./install.sh`
unter unix mit systemd

### Ausführen
Über `python cli.py -h`können alle Subkommandos aufgelistet werden. 

`python cli.py status -h` listet alle optionalen Argumente für eine Statusübersicht auf.
z.B. `python cli.py status -a` zeigt die Übersicht über alle Router an
     `python cli.py status -r [VLAN ID]` zeigt detaillierte Infos zu einem bestimmten Router an, der sich
     im VLAN mit der gegebenen ID befindet.
     

_Konventionen, Vorgehensweise und Dokumentation im Wiki_

![Class Diagram](http://plantuml.com/plantuml/svg/3SSx3i8m303Ggy05ufsD4xG3UsLSAx68dSeVSNrusxkBqQoJo-TjP5xn073yjYuvwbt1JikIBHijXRsqw3CtUmr-YiFc7Kq2Sxa43GvGZ6G7cXXnbCxZ5EoEsgv_VW00?lol12)

