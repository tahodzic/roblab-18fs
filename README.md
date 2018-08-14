# Winston - Der Servierroboter
Projekt für das Modul "Cognitive Robotics Lab" der Hochschule Luzern Department Informatik.
Behaviour für den Pepper Roboter von der Firma Softbank, welches in einer Umgebung (bspw. Restaurants) zu vordefinierten Tischen auf Abruf fährt und dem rufenden Kunden eine Menükarte auf dem Tablet anzeigt.
Die Bestellung wird vom Kunden über das Tablet getätigt, nach Abschluss fährt Pepper zurück an den Anfangspunkt.

## Getting Started

1. MongoDB starten
* Über Terminal (cmd, ...) ins MongoDB-Verzeichnis navigieren und dort mongod.exe ausführen.
2. Webserver starten, dazu mit Terminal ins Verzeichnis navigieren, wo mainpage.js ist und folgenden Befehl ausführen:
```
node .\mainpage.js
```
3. Ein Terminalfenster bereithalten, welches den Client für den Rufknopf aufruft (client.py)
4. Pepper an einem idealen Ort im Raum ausrichten, typischerweise vor der Tür, damit der Kunde empfangen werden kann.
5. Mit Filezilla oder ähnlichem Programm main.py auf den Pepper kopieren
6. Über SSH (Putty, ...) auf Pepper verbinden
7. Mit folgendem Befehl Behaviour starten:
```
python main.py
```

### Voraussetzungen

Für das komplette Behaviour mit Menükarte wird Folgendes benötigt:
* Python für client.py auf eigenem PC (Simulation des Rufknopfs)
* MongoDB, beinhaltet Tischpositionen, Gerichte und Bestellungen
* Node.js, hostet die Webseite (Menükarte) und greift auf MongoDB zu
* client.py aus Repo, welches den Rufknopf auf dem Tisch simuliert
* Fertiges Map Exploration File (siehe /map) oder eine eigene Exploration kann gestartet werden, siehe dazu: http://doc.aldebaran.com/2-5/naoqi/motion/exploration-api.html


### Installation
1. MongoDB installieren und fertige Datenbank aus /db runterlanden und ins eigene Datenbankverzeichnis kopieren (typischerweise C:\data\db unter Windows und /data/db unter Linux)
* Siehe https://docs.mongodb.com/manual/installation/
2. Node.js installieren
* Siehe https://nodejs.org/en/download/package-manager/
3. Anschliessend Express.js installieren, folgende Anleitung beachten: http://expressjs.com/de/starter/installing.html
4. Danach den MongoDB Treiber für Node.js installieren, folgende Anleitung beachten: https://www.npmjs.com/package/mongodb

## Autoren

* **Damir Hodzic**
* **Sukirthan Kasipillai (https://github.com/Xeuks)**
