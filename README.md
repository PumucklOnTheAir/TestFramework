[![Build Status](https://travis-ci.org/PumucklOnTheAir/TestFramework.svg?branch=master)](https://travis-ci.org/PumucklOnTheAir/TestFramework)
[![codecov.io](https://codecov.io/github/PumucklOnTheAir/TestFramework/coverage.svg?branch=master)](https://codecov.io/github/PumucklOnTheAir/TestFramework?branch=master)
[![codecov.io](https://readthedocs.org/projects/freifunk-testframework/badge)](https://freifunk-testframework.readthedocs.org)

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

### Testen
Eine Auswahl an Unittest fürs Framwork wird bei jedem Pull-Request auf Travis CI ausgeführt.
Eine vollständiges Testens des Frameworks ist auf dem Raspberry Pi möglich mit folgendem Kommando im Repo Ordner:
python -m unittest discover -s framework_unittests

