#!/usr/bin/env python3
"""Metadata-only YouTube playlist catalog. Never downloads video or audio."""
import argparse, json, pathlib, subprocess, sys, datetime

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--url",required=True)
    p.add_argument("--limit",type=int,default=10)
    p.add_argument("--output",default="data/catalog/first-10.json")
    args=p.parse_args()
    if not 1 <= args.limit <= 500: p.error("limit must be between 1 and 500")
    cmd=[sys.executable,"-m","yt_dlp","--flat-playlist","--dump-single-json","--playlist-end",str(args.limit),"--skip-download","--no-warnings",args.url]
    proc=subprocess.run(cmd,text=True,capture_output=True,timeout=240)
    if proc.returncode: raise SystemExit("Metadata fetch failed: "+proc.stderr[-2000:])
    raw=json.loads(proc.stdout)
    entries=[]
    for i,e in enumerate(raw.get("entries") or [],1):
        if not e: continue
        vid=e.get("id")
        entries.append({"position":i,"id":vid,"title":e.get("title"),"duration_seconds":e.get("duration"),"url":("https://www.youtube.com/watch?v="+vid) if vid else e.get("url"),"transcript_status":"not_checked","media_status":"not_imported"})
    data={"playlist_url":args.url,"playlist_title":raw.get("title"),"declared_count":raw.get("playlist_count"),"requested_limit":args.limit,"fetched_count":len(entries),"videos":entries}
    target=pathlib.Path(args.output);target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"Saved {len(entries)} videos to {target}")
if __name__=="__main__": main()
