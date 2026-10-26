# Audio import workflow

The supplied folder currently contributes 84 unique OGG Vorbis tracks to the mod. The importer stores copies under `src/main/resources/assets/caribbean_shanties/sounds/shanties`, creates jukebox song data, updates disc translations, and records source details in `shanty_manifest.csv`. It leaves the input folder unchanged.

Run `py "$env:TEMP\caribbean-shanties\tools\import_shanties.py"` after adding additional OGG Vorbis files to the specified music folder. Non-Vorbis OGG files are rejected so they are not mislabeled as Minecraft-compatible.
