# HANDOFF — Chubak Aju 80

## Current state
- Repo initialized separately from lesson-80.
- First target: first 10 entries of playlist PLC-unxVGahSmS7NuDTU4m8L-9eEgCYMXa.
- Metadata-only GitHub Actions workflow available for manual dispatch.
- No video files or transcripts downloaded, no R2 secrets configured, no rendered lessons.

## Next steps
1. Run Actions → Catalog YouTube playlist → Run workflow, limit=10.
2. Inspect artifact playlist-catalog and confirm actual titles, durations, IDs and playlist order. Some YouTube playlists may block automated extraction.
3. Decide source access/permission for original media. Avoid downloading copyrighted videos without authorization.
4. Build transcript pipeline with explicit missing/unavailable statuses and source attribution.
5. Group by topic; related imam Q&A included, unrelated Q&A omitted.
6. Check theological sources and produce a child-friendly Kyrgyz script for one 60-minute pilot, without padding.

## Constraints
- Age 4–12; 2D; no background music by default; clear Kyrgyz speech.
- No unverified hadith or invented quotations.
- No paid rendering or paid API calls without approval.
- R2 secrets only in GitHub Actions Secrets, never commit credentials.
