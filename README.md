# Caribbean Shanties (Fabric 26.2)

A Fabric 26.2 mod that adds collectible, jukebox-playable shanty discs. Each creeper has a 10% chance to drop one of the discs when a skeleton gets the kill. Vanilla structure chest loot tables receive an additive 2% chance pool containing one random shanty disc; third-party chest tables are left unchanged.

Custom jukebox playback is patched so the client keeps playing while a disc remains inserted and stops immediately when the disc is removed. See `THIRD_PARTY_NOTICES.md` for the upstream implementation credit and license.

Every disc has an original generated pixel-art texture. In-game item names use the requested game suffix. The jukebox now-playing credit displays Artist - Song; Resynced source filenames provide Seán Dagher or Sarah Greene where credited, while the supplied original-game files lack individual artist tags and use the album credit Various Artists.

## Imported audio

The project imported 84 unique tracks from the Assassin's Creed Series. All 85 source files were identified as OGG Vorbis, copied without re-encoding, and left unchanged.
No filenames in the supplied folder identify a Freedom Cry track, so this import contains no Freedom Cry audio.


## Build

Requires JDK 25+ and network access for Gradle dependencies. The project targets Minecraft 26.2, Fabric Loader 0.19.3, Fabric API 0.155.2+26.2, Loom 1.17.21, and Gradle 9.5.1. Generate a wrapper with gradle wrapper --gradle-version 9.5.1, then run gradlew.bat build.
