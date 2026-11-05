#!/usr/bin/env python3
"""Inspect available captions for one YouTube video without downloading media."""
import argparse
import datetime
import json
import pathlib
import yt_dlp

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--video-id", default="0zX-T97PRK8")
    parser.add_argument("--output", default="data/captions/lesson-001-availability.json")
    args = parser.parse_args()
    result = {
        "video_id": args.video_id,
        "video_url": "https://www.youtube.com/watch?v=" + args.video_id,
        "checked_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "status": "pending",
        "manual_captions": {},
        "automatic_captions": {},
    }
    try:
        with yt_dlp.YoutubeDL({
            "quiet": True,
            "no_warnings": True,
            "skip_download": True,
            "extract_flat": False,
            "ignoreerrors": False,
            "retries": 1,
            "socket_timeout": 20,
        }) as ydl:
            info = ydl.extract_info(result["video_url"], download=False)
        result["title"] = info.get("title")
        result["duration_seconds"] = info.get("duration")
        for key, target in [("subtitles", "manual_captions"), ("automatic_captions", "automatic_captions")]:
            result[target] = {
                lang: sorted(set(item.get("ext", "unknown") for item in tracks))
                for lang, tracks in (info.get(key) or {}).items()
            }
        result["status"] = "checked"
    except Exception as exc:
        result["status"] = "unavailable"
        result["error"] = str(exc)[:1000]
    out = pathlib.Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Caption availability status:", result["status"])
    print("Manual languages:", ", ".join(result["manual_captions"]) or "none")
    print("Auto languages:", ", ".join(result["automatic_captions"]) or "none")
    if result["status"] != "checked":
        raise SystemExit("YouTube caption inspection unavailable; see artifact for details")

if __name__ == "__main__":
    main()
