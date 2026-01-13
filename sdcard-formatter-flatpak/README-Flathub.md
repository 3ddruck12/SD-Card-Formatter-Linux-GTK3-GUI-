# Flathub Submission Guide

## Vorbereitete Dateien für Flathub:

✅ `org.sdcard.Formatter.yaml` - Flatpak Manifest
✅ `org.sdcard.Formatter.metainfo.xml` - AppStream Metadaten
✅ `sdcard-formatter.desktop` - Desktop Entry
✅ `sd_formatter_gui.py` - Hauptanwendung
✅ `sdcard-formatter.png` - Icon (256x256)

## Schritte zur Einreichung bei Flathub:

### 1. Fork das Flathub Repository
```bash
# Auf GitHub: Fork https://github.com/flathub/flathub
```

### 2. Erstelle einen Pull Request
```bash
# In deinem Fork:
mkdir org.sdcard.Formatter
cp sdcard-formatter-flatpak/org.sdcard.Formatter.yaml org.sdcard.Formatter/
cp sdcard-formatter-flatpak/org.sdcard.Formatter.metainfo.xml org.sdcard.Formatter/
# Weitere Dateien nach Bedarf
```

### 3. Manifest aktualisieren
Die Manifest-Datei muss auf das GitHub-Repository verweisen:
```yaml
sources:
  - type: git
    url: https://github.com/3ddruck12/SD-Card-Formatter-Linux-GTK3-GUI-.git
    tag: v1.0.5
```

### 4. Flathub Anforderungen prüfen:
- ✅ Lizenz angegeben (GPL-3.0+)
- ✅ AppStream Metainfo vorhanden
- ✅ Desktop Entry korrekt
- ✅ Icon in korrekter Größe
- ⚠️ Screenshot im Repository (bereits vorhanden)

### 5. Lokal testen:
```bash
cd sdcard-formatter-flatpak
flatpak-builder --user --install --force-clean build-dir org.sdcard.Formatter.yaml
flatpak run org.sdcard.Formatter
```

### 6. Qualitätskontrolle:
```bash
flatpak run --command=flatpak-builder-lint org.flatpak.Builder appstream org.sdcard.Formatter.metainfo.xml
flatpak run --command=flatpak-builder-lint org.flatpak.Builder manifest org.sdcard.Formatter.yaml
```

## Wichtige Hinweise:

- Das `format_sd` Binary wird NICHT mit Flatpak gebündelt (Lizenzgründe)
- Der First-Run-Dialog führt den Benutzer durch den Download
- Die App benötigt `--device=all` für Hardware-Zugriff

## Weitere Informationen:
https://docs.flathub.org/docs/for-app-authors/submission
