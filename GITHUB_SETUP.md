# GitHub Setup und Deployment Anleitung

## Repository auf GitHub hochladen

### 1. Git initialisieren (falls noch nicht geschehen)
```bash
cd "/home/jens/Dokumente/Software Projekte/sdcardformatter_gui"
git init
git add .
git commit -m "Initial commit"
```

### 2. Remote Repository hinzufügen
```bash
git remote add origin https://github.com/3ddruck12/SD-Card-Formatter-Linux-GTK3-GUI-.git
git branch -M main
git push -u origin main
```

## GitHub Actions

Die folgenden Workflows wurden eingerichtet:

### 1. **Build DEB Package** (`.github/workflows/build-deb.yml`)
- Wird ausgeführt bei jedem Push auf `main`/`master`
- Baut automatisch das .deb Paket
- Lädt das Paket als Artifact hoch
- Erstellt ein Release bei Tags (z.B. `v1.0.0`)

### 2. **Build Flatpak** (`.github/workflows/build-flatpak.yml`)
- Wird ausgeführt bei jedem Push auf `main`/`master`
- Baut automatisch das Flatpak-Paket
- Lädt das Paket als Artifact hoch
- Erstellt ein Release bei Tags (z.B. `v1.0.0`)

### 3. **Create Release** (`.github/workflows/release.yml`)
- Wird nur bei Tags ausgeführt
- Erstellt einen Release mit Beschreibung

## Pakete herunterladen

### Nach jedem Push
Die gebauten Pakete findest du unter:
- **Actions** Tab in GitHub
- Wähle den entsprechenden Workflow Run
- Unter **Artifacts** kannst du die Pakete herunterladen

### Bei Releases
1. Release erstellen mit Tag:
```bash
git tag v1.0.0
git push origin v1.0.0
```

2. Die Pakete werden automatisch zum Release hinzugefügt unter:
   `https://github.com/3ddruck12/SD-Card-Formatter-Linux-GTK3-GUI-/releases`

## Manueller Workflow-Start

Du kannst die Workflows auch manuell starten:
1. Gehe zu **Actions** Tab in GitHub
2. Wähle den Workflow aus
3. Klicke auf **Run workflow**
4. Wähle den Branch und starte

## Lokale Tests

### DEB Paket lokal bauen
```bash
cd sdcard-formatter-deb
./build-deb.sh
```

### Flatpak lokal bauen
```bash
cd sdcard-formatter-flatpak
./build-flatpak.sh
```

## Fehlerbehebung

### GitHub Actions schlagen fehl?
- Überprüfe die Logs unter **Actions** Tab
- Stelle sicher, dass alle Dateien korrekt committet sind
- Überprüfe, ob die Pfade in den Workflows korrekt sind

### Flatpak Build Fehler?
- Der Workflow verwendet einen speziellen Container für Flatpak-Builds
- Stelle sicher, dass alle benötigten Dateien im `sdcard-formatter-flatpak/` Verzeichnis vorhanden sind

### Permissions Fehler?
- GitHub Actions haben automatisch Zugriff auf das Repository
- Für Releases wird `GITHUB_TOKEN` automatisch bereitgestellt
