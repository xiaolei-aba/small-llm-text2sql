"""Download the exact archive linked by the official Spider 1.0 website."""

import argparse
import hashlib
import json
import shutil
import sys
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OFFICIAL_PAGE = "https://yale-lily.github.io/spider"
FILE_ID = "1403EGqzIDoHMdQF4c9Bkyl7dZLZ5Wt6J"
DOWNLOAD_URL = f"https://drive.usercontent.google.com/download?id={FILE_ID}&export=download&confirm=t"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--proxy", default=None)
    parser.add_argument("--reuse-archive", action="store_true",
                        help="Resume extraction from the existing ZIP; verify existing file contents")
    args = parser.parse_args()
    if Path(sys.prefix).name != "text2sql":
        raise RuntimeError("Use the text2sql environment")
    gate = json.loads((ROOT / "docs" / "cuda_check.json").read_text(encoding="utf-8"))
    if not gate["passed"]:
        raise RuntimeError("CUDA gate has not passed")
    cache = ROOT / "cache" / "downloads"
    cache.mkdir(parents=True, exist_ok=True)
    archive = cache / "spider_data.zip"
    part = cache / "spider_data.zip.part"
    output = ROOT / "data" / "raw" / "spider"
    if output.exists() and any(output.iterdir()) and not args.reuse_archive:
        raise FileExistsError("Refuse to overwrite existing raw data")
    handlers = []
    if args.proxy:
        handlers.append(urllib.request.ProxyHandler({"https": args.proxy, "http": args.proxy}))
    opener = urllib.request.build_opener(*handlers)
    metadata = {"official_page": OFFICIAL_PAGE,
                "official_link": f"https://drive.google.com/file/d/{FILE_ID}/view",
                "download_url": DOWNLOAD_URL,
                "download_started_at_utc": datetime.now(timezone.utc).isoformat(),
                "dataset": "Spider 1.0", "license": "CC-BY-SA-4.0",
                "license_source": OFFICIAL_PAGE}
    if args.reuse_archive:
        with archive.open("rb") as stream:
            digest = hashlib.file_digest(stream, "sha256")
        received = archive.stat().st_size
        metadata["reused_download"] = True
        metadata["download_completed_at_utc"] = datetime.fromtimestamp(
            archive.stat().st_mtime, timezone.utc).isoformat()
    else:
        digest = hashlib.sha256()
        received = 0
        with opener.open(DOWNLOAD_URL, timeout=90) as response, part.open("wb") as stream:
            metadata["last_modified"] = response.headers.get("Last-Modified")
            metadata["content_length"] = response.headers.get("Content-Length")
            metadata["content_disposition"] = response.headers.get("Content-Disposition")
            next_progress = 16 * 1024 * 1024
            while chunk := response.read(1024 * 1024):
                stream.write(chunk)
                digest.update(chunk)
                received += len(chunk)
                if received >= next_progress:
                    print(f"Downloaded {received / 1024**2:.0f} MiB", flush=True)
                    next_progress += 16 * 1024 * 1024
        if metadata["content_length"] and received != int(metadata["content_length"]):
            raise RuntimeError("Incomplete download")
        if not zipfile.is_zipfile(part):
            raise RuntimeError("Official download did not return a ZIP archive; inspect before retry")
        part.replace(archive)
    metadata.update(archive_sha256=digest.hexdigest(), archive_bytes=received,
                    extraction_at_utc=datetime.now(timezone.utc).isoformat())
    metadata["skipped_members"] = []
    output.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive) as bundle:
        bad = bundle.testzip()
        if bad:
            raise RuntimeError(f"CRC failed: {bad}")
        metadata["archive_members"] = bundle.namelist()
        # Preserve member names. Audit first rather than guessing or renaming splits.
        for info in bundle.infolist():
            if any(c in info.filename for c in ':*?<>|'):
                metadata["skipped_members"].append({"path": info.filename,
                    "reason": "Windows-incompatible filename; original retained inside ZIP"})
                continue
            target = (output / info.filename).resolve()
            if not target.is_relative_to(output.resolve()):
                raise ValueError(f"Unsafe archive member: {info.filename}")
            if info.is_dir():
                target.mkdir(parents=True, exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                if target.exists():
                    with bundle.open(info) as source, target.open("rb") as existing:
                        if hashlib.file_digest(source, "sha256").digest() != hashlib.file_digest(existing, "sha256").digest():
                            raise RuntimeError(f"Existing file differs; refuse overwrite: {target}")
                    continue
                with bundle.open(info) as source, target.open("xb") as dest:
                    shutil.copyfileobj(source, dest)
    metadata["extraction_root"] = str(output)
    (ROOT / "data" / "manifests" / "spider_download.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in metadata.items() if k != "archive_members"}, indent=2))
    print("Top-level entries:", sorted(p.name for p in output.iterdir()))


if __name__ == "__main__":
    main()
