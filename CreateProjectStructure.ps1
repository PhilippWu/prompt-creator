# Ermitteln des Verzeichnisses, in dem dieses Skript liegt
$root = $PSScriptRoot

# Liste der zu erstellenden Verzeichnisse (relative Pfade)
$directories = @(
    "$root\src",
    "$root\resources",
    "$root\tests",
    "$root\docs",
    "$root\.github\workflows"
)

# Erstelle alle Verzeichnisse, sofern sie noch nicht existieren
foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -Path $dir -ItemType Directory | Out-Null
    }
}

# Liste der zu erstellenden Dateien mit Pfadangaben (relative Pfade)
$files = @(
    "$root\src\__init__.py",
    "$root\src\main.py",            # Hauptanwendung (GUI-Code, z.B. Tkinter)
    "$root\resources\Config.json",  # Konfigurationsdatei (z.B. zuletzt genutzter Projektordner)
    "$root\resources\Exclude.json", # Exclude-Datei (editierbar über die GUI)
    "$root\tests\__init__.py",
    "$root\tests\test_main.py",      # Unit-Tests für die Module
    "$root\docs\README.md",          # Dokumentation, Architektur, etc.
    "$root\.github\workflows\release.yml", # GitHub Actions Workflow für automatisierte Releases
    "$root\requirements.txt",        # Abhängigkeiten (z.B. tkinter, pyinstaller, ...)
    "$root\README.md",               # Projektbeschreibung und Anleitung
    "$root\setup.py"                 # (Optional) Für Packaging/Installation
)

# Erstelle alle Dateien (leere Dateien, falls sie noch nicht existieren)
foreach ($file in $files) {
    if (-not (Test-Path $file)) {
        New-Item -Path $file -ItemType File | Out-Null
    }
}

Write-Host "Projektstruktur wurde im Root-Verzeichnis '$root' erstellt."
