#!/usr/bin/env python3
"""Convert locally supplied audio/video files to Minecraft-ready OGG Vorbis.

This tool intentionally processes local files only. It does not fetch music from
YouTube or other streaming services. Place audio you are authorized to use in
the configured input directory, then run this script again to resume safely.
"""
from __future__ import annotations
import argparse, hashlib, json, os, re, shutil, subprocess, sys, tempfile, unicodedata
from pathlib import Path

DEFAULT_DIR = Path(r"C:\Users\Ekagra\Downloads\Mod Work\Shanties Music Discs")
SUPPORTED = {".aac", ".aif", ".aiff", ".flac", ".m4a", ".mka", ".mkv", ".mov", ".mp3", ".mp4", ".ogg", ".opus", ".wav", ".webm", ".wma"}
MANIFEST = "shanty_manifest.csv"


def norm_title(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch)).lower()
    text = re.sub(r"\b(official|audio|video|lyrics?|soundtrack|ost|hq|hd|4k)\b", " ", text)
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def run_capture(args: list[str]) -> bytes:
    p = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if p.returncode:
        raise RuntimeError(p.stderr.decode("utf-8", "replace")[-2000:])
    return p.stdout


def probe(path: Path, ffprobe: str) -> dict:
    data = json.loads(run_capture([ffprobe, "-v", "error", "-select_streams", "a:0", "-show_entries", "stream=codec_name,channels,sample_rate,bit_rate:format=duration,bit_rate", "-of", "json", str(path)]))
    streams = data.get("streams", [])
    if not streams:
        raise RuntimeError("No audio stream found")
    return {**streams[0], **data.get("format", {})}


def pcm_fingerprint(path: Path, ffmpeg: str) -> str:
    # Canonical decoded audio hash catches format/container changes without
    # adding third-party fingerprint packages. Similar-but-different masters
    # remain separate; duplicate detection also uses normalized filenames.
    p = subprocess.Popen([ffmpeg, "-v", "error", "-i", str(path), "-map", "0:a:0", "-vn", "-ac", "1", "-ar", "11025", "-f", "s16le", "-"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    h = hashlib.sha256()
    assert p.stdout is not None
    for chunk in iter(lambda: p.stdout.read(1024 * 1024), b""):
        h.update(chunk)
    err = p.stderr.read() if p.stderr else b""
    if p.wait() != 0:
        raise RuntimeError(err.decode("utf-8", "replace")[-2000:])
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, default=DEFAULT_DIR)
    parser.add_argument("--quality", type=int, choices=range(0, 11), default=8)
    args = parser.parse_args()
    folder = args.input_dir.expanduser().resolve()
    folder.mkdir(parents=True, exist_ok=True)
    manifest = folder / MANIFEST
    import csv
    columns = ["title", "normalized_title", "input_file", "output_file", "status", "codec", "channels", "sample_rate", "duration_seconds", "sha256", "audio_fingerprint", "duplicate_of", "details"]
    files = sorted((p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in SUPPORTED and p.name.lower() != MANIFEST), key=lambda p: p.name.casefold())
    ffmpeg, ffprobe = shutil.which("ffmpeg"), shutil.which("ffprobe")
    rows = []
    # Use atomic manifest replacement so an interruption cannot corrupt progress.
    if not ffmpeg or not ffprobe:
        for src in files:
            title = src.stem
            rows.append(dict(title=title, normalized_title=norm_title(title), input_file=str(src), output_file="", status="blocked_missing_ffmpeg", codec="", channels="", sample_rate="", duration_seconds="", sha256="", audio_fingerprint="", duplicate_of="", details="Install FFmpeg (ffmpeg and ffprobe) and rerun; no input files were changed."))
        write_manifest(manifest, columns, rows)
        print(f"Blocked: ffmpeg={bool(ffmpeg)}, ffprobe={bool(ffprobe)}. Manifest: {manifest}. Local files found: {len(files)}")
        return 2 if files else 0

    existing_by_title: dict[str, Path] = {}
    fingerprints: dict[str, Path] = {}
    for p in sorted(folder.glob("*.ogg"), key=lambda p: p.name.casefold()):
        if p.name.lower() == MANIFEST:
            continue
        try:
            meta = probe(p, ffprobe)
            if meta.get("codec_name") == "vorbis":
                existing_by_title.setdefault(norm_title(p.stem), p)
                fingerprints.setdefault(pcm_fingerprint(p, ffmpeg), p)
        except Exception:
            continue

    for src in files:
        title, normalized = src.stem, norm_title(src.stem)
        if src.suffix.lower() == ".ogg":
            try:
                meta = probe(src, ffprobe)
                status = "already_vorbis" if meta.get("codec_name") == "vorbis" else "source_ogg_not_vorbis"
                rows.append(make_row(src, src if status == "already_vorbis" else None, title, normalized, status, meta, details="Kept source file unchanged."))
            except Exception as e:
                rows.append(make_row(src, None, title, normalized, "invalid_audio", {}, details=str(e)))
            continue
        if not normalized:
            rows.append(make_row(src, None, title, normalized, "invalid_filename", {}, details="Could not derive a safe title from filename.")); continue
        if normalized in existing_by_title:
            rows.append(make_row(src, existing_by_title[normalized], title, normalized, "existing_title_preserved", {}, details="Existing OGG kept unchanged; no overwrite.")); continue
        with tempfile.TemporaryDirectory(prefix="shanty-convert-") as td:
            temp = Path(td) / "converted.ogg"
            p = subprocess.run([ffmpeg, "-nostdin", "-hide_banner", "-loglevel", "error", "-y", "-i", str(src), "-map", "0:a:0", "-vn", "-c:a", "libvorbis", "-q:a", str(args.quality), str(temp)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if p.returncode or not temp.exists() or temp.stat().st_size == 0:
                rows.append(make_row(src, None, title, normalized, "conversion_failed", {}, details=p.stderr.decode("utf-8", "replace")[-2000:])); continue
            try:
                meta = probe(temp, ffprobe)
                duration = float(meta.get("duration", 0))
                if meta.get("codec_name") != "vorbis": raise RuntimeError(f"Unexpected codec: {meta.get('codec_name')}")
                if duration < 5: raise RuntimeError(f"Unexpectedly short audio: {duration:.2f} seconds")
                fingerprint = pcm_fingerprint(temp, ffmpeg)
                if fingerprint in fingerprints:
                    rows.append(make_row(src, fingerprints[fingerprint], title, normalized, "duplicate_audio", meta, fingerprint=fingerprint, details="Decoded audio matches an existing OGG; duplicate not copied.")); continue
                output = folder / f"{normalized.replace(' ', '_')}.ogg"
                if output.exists():
                    rows.append(make_row(src, output, title, normalized, "existing_output_preserved", meta, fingerprint=fingerprint, details="Output filename already exists; existing file left untouched.")); continue
                shutil.copy2(temp, output)
                verified = probe(output, ffprobe)
                if verified.get("codec_name") != "vorbis":
                    output.unlink(missing_ok=True)
                    raise RuntimeError("Post-copy verification failed: codec is not Vorbis")
                fp = pcm_fingerprint(output, ffmpeg)
                fingerprints[fp] = output
                existing_by_title[normalized] = output
                rows.append(make_row(src, output, title, normalized, "converted_verified", verified, fingerprint=fp, details=f"FFmpeg libvorbis quality {args.quality}; source retained."))
            except Exception as e:
                rows.append(make_row(src, None, title, normalized, "verification_failed", {}, details=str(e)))
        write_manifest(manifest, columns, rows)
    write_manifest(manifest, columns, rows)
    counts = {}
    for row in rows: counts[row["status"]] = counts.get(row["status"], 0) + 1
    print(json.dumps({"directory": str(folder), "input_files": len(files), "results": counts, "manifest": str(manifest)}, indent=2))
    return 0


def make_row(src: Path, out: Path | None, title: str, normalized: str, status: str, meta: dict, fingerprint: str = "", details: str = "") -> dict:
    return {"title": title, "normalized_title": normalized, "input_file": str(src), "output_file": str(out) if out else "", "status": status, "codec": meta.get("codec_name", ""), "channels": meta.get("channels", ""), "sample_rate": meta.get("sample_rate", ""), "duration_seconds": meta.get("duration", ""), "sha256": sha256(out) if out and out.exists() else "", "audio_fingerprint": fingerprint, "duplicate_of": str(out) if status == "duplicate_audio" and out else "", "details": details}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""): h.update(chunk)
    return h.hexdigest()


def write_manifest(path: Path, columns: list[str], rows: list[dict]) -> None:
    import csv
    temp = path.with_suffix(".csv.tmp")
    with temp.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader(); writer.writerows(rows)
    os.replace(temp, path)

if __name__ == "__main__":
    raise SystemExit(main())
