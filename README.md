# Bewerbung

Das Repository Bewerbung enthält Daten und Skripte zum Erzeugen von Bewerbungen.


Eine Bewerbung besteht aus:

  - Anschreiben
  - Lebenslauf
  - Anlagen z.B.:
     - Zeugnisse
     - Referenzen
     - eventuell sonstigen Dokumenten


  Der Prozess des Erzeugens einer Bewerbung erfolgt in mehreren Schritten.

  1. Lesen des Profils im Verzeichnis Profil. Dateien in diesem Verzeichnis folgen dem Muster YYYYMMDD.* . 
     Es wird die Neueste (gemäß dem Muster) gelesen.

  2. Lesen der Stellenbeschreibung im Verzeichnis Stellenbeschreibung. Dateien in diesem Verzeichnis folgen dem Muster YYYYMMDD.* . 
     Es wird die Neueste (gemäß dem Muster) gelesen.  

  3. Basierend auf den Namen der Profile und Stellenbeschreibungsdatei wird ein Ausgabeverzeichniserzeugt. 
     Ist der Name der Profildatei 202506006_profil.pdf und der Name der Stellenbeschreibungsdatei 202506006_stelle.txt so 
     lautet der Name des Ausgabeverzeichnisses 202506006_stelle-202506006_profil. 
     Der Pfad zum Ausgabeverzeichnis wäre Ausgabe/202506006_stelle-202506006_profil. 

  4. Im Ausgabeverzeichnis werden die Dateien für:

      - Anschreiben 
      - Lebenslauf
      - Anlagen

      erzeugt.

  5. Im Ausgabeverzeichnis wird ein Ordner pdf erzeugt.

  6. Die Dateien im Ausgabeverzeichnis werden im Format pdf erzeugt und in dem Ordner pdf abgelegt.




Hints:

 ```
brew install cffi fonttools pango pillow six
```

