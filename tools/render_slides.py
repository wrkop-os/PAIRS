#!/usr/bin/env python3
"""Render each project's real presentation deck to slide images.

Downloads the decks from Google Drive, converts them with LibreOffice, and
rasterises every page to `uploads/slides/P-XX/NN.webp`. The site prefers these
images over the text rendering whenever they exist (see tools/build-content.py).

This is meant to run on a GitHub Actions runner, which — unlike the agent
sandbox — can reach Google Drive. It needs the Drive folder to be shared as
"Anyone with the link → Viewer"; the files are fetched anonymously.

    python3 tools/render_slides.py            # all decks
    python3 tools/render_slides.py P-01 P-05  # just these
"""
import shutil
import subprocess
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "uploads" / "slides"
WORK = ROOT / ".slide-build"

# Project ID -> (Drive file ID, original file name). Mirrors the sourceFile
# entries in the design data; see content/decks/README.md.
DECKS = {
    "P-01": ("1MZWFSsC-hBtEpQDy1VpjL6ejtlGsKbum", "AI Detection Ensemble.pptx"),
    "P-02": ("1b5Oun_MUxdxxPvJrUw9aODSJpzqQrhmO", "Ml slides.pptx"),
    "P-03": ("1gEgUnJve1K-Pnh4LNxWLQFsTDM9coBRu", "battery_rul_presentation.pptx"),
    "P-04": ("1-y6qGcLpo5YZIaJFSm1iqXZ8t1b-7R5C", "Multi-Chemistry Battery Voltage.pptx"),
    "P-05": ("1TPATWOZiCLEcx56fWSpAQtU8LkL5blFZ", "Timescale-Aware Neural ODEs.pptx"),
    "P-06": ("1NkhPOORG1rzPpOLfQY4myeVQs7R-YNGI", "Areeb PAIRS Slideshow.pptx"),
    "P-07": ("1aDIF9gSxtfPy6yWRVpqhR_ivl_SY-1wp", "Predicting EMI in Circuit Boards.pptx"),
    "P-08": ("12XMZym2VIUE4dqpUlLiIuZSPyiqfTIDB", "Full_Project_Presentation.pptx"),
    "P-09": ("1LRpsziLXjkreed-XEjT4xtUKW1ScqRvV", "PAIRS.pptx"),
    "P-10": ("1P4euzWpnnFStqAdhxkxpAWEXeh_2CzQb", "Tirtha Saha - Final Presentation.pptx"),
    "P-11": ("1ifpB0-tAxAwb8AKlL488QunoqikP05Zt", "Can-We-Predict-What-Goes-Viral.pptx"),
    "P-12": ("1ExH751_hyVbZnaSp7CAZap5utbYIVreZ", "PAIRS_PINN_Cylinder_Flow.pdf"),
}

# The viewer's stage is ~1100px wide; 1600 keeps it crisp on a retina screen
# without making the repository enormous.
WIDTH = 1600
QUALITY = 80


class AccessError(RuntimeError):
    """The deck could not be fetched because the Drive folder is not shared."""


def download(file_id, dest):
    """Fetch a Drive file anonymously. Requires link sharing on the folder."""
    import gdown
    url = f"https://drive.google.com/uc?id={file_id}"
    try:
        gdown.download(url, str(dest), quiet=True)
    except Exception as exc:
        # gdown raises its own FileURLRetrievalError when Drive refuses an
        # anonymous fetch. That is the not-shared case, not a broken build.
        text = str(exc)
        if "public link" in text or "permission" in text or "Permission" in text:
            raise AccessError(
                f"Drive refused an anonymous download of {file_id}: the folder "
                f"is not shared as 'Anyone with the link'"
            ) from exc
        raise
    if not dest.exists() or dest.stat().st_size == 0:
        raise AccessError(
            f"download produced no file for {file_id} — the Drive folder is "
            f"not shared as 'Anyone with the link'"
        )
    # Drive serves an HTML interstitial instead of the file when access is
    # denied, which would otherwise reach LibreOffice as a corrupt deck.
    head = dest.open("rb").read(200).lstrip()
    if head[:1] == b"<":
        raise AccessError(
            f"Drive returned its sign-in page, not a file, for {file_id} — the "
            f"folder is still private"
        )


def to_pdf(src, outdir):
    if src.suffix.lower() == ".pdf":
        return src
    subprocess.run(
        ["soffice", "--headless", "--norestore", "--convert-to", "pdf",
         "--outdir", str(outdir), str(src)],
        check=True, capture_output=True, timeout=600,
    )
    pdf = outdir / (src.stem + ".pdf")
    if not pdf.exists():
        raise RuntimeError(f"LibreOffice produced no PDF for {src.name}")
    return pdf


def rasterise(pdf, dest_dir):
    import pypdfium2
    dest_dir.mkdir(parents=True, exist_ok=True)
    for old in dest_dir.glob("*.webp"):
        old.unlink()
    doc = pypdfium2.PdfDocument(str(pdf))
    written = []
    for i in range(len(doc)):
        page = doc[i]
        scale = WIDTH / page.get_width()
        image = page.render(scale=scale).to_pil().convert("RGB")
        path = dest_dir / f"{i + 1:02d}.webp"
        image.save(path, "WEBP", quality=QUALITY, method=6)
        written.append(path)
    return written


def main(only):
    WORK.mkdir(exist_ok=True)
    total_bytes = 0
    total_slides = 0
    failures = []
    denied = []
    for pid, (file_id, name) in sorted(DECKS.items()):
        if only and pid not in only:
            continue
        try:
            src = WORK / f"{pid}{pathlib.Path(name).suffix}"
            download(file_id, src)
            pdf = to_pdf(src, WORK)
            written = rasterise(pdf, OUT / pid)
            size = sum(p.stat().st_size for p in written)
            total_bytes += size
            total_slides += len(written)
            print(f"{pid}: {len(written):3d} slides  {size / 1024:7.0f} KB  ({name})")
        except AccessError as exc:
            denied.append(f"{pid}: {exc}")
            print(f"{pid}: no access — {exc}", file=sys.stderr)
        except Exception as exc:  # keep going; report every failure at the end
            failures.append(f"{pid}: {exc}")
            print(f"{pid}: FAILED — {exc}", file=sys.stderr)
    shutil.rmtree(WORK, ignore_errors=True)
    print(f"\ntotal: {total_slides} slides, {total_bytes / 1024 / 1024:.1f} MB")

    if failures:
        print("\nfailures:", file=sys.stderr)
        for f in failures:
            print("  -", f, file=sys.stderr)
        return 1

    # Nothing rendered because the source folder is not readable yet. That is a
    # waiting-on-access state, not a broken build — the toolchain above it has
    # just been exercised, so report it and exit clean.
    if denied and not total_slides:
        print(
            "\nNo decks could be fetched: the Drive folder is not shared.\n"
            "Set it to 'Anyone with the link -> Viewer' and re-run this workflow:\n"
            "  https://drive.google.com/drive/folders/1L_wC6d70zFuG8VAIq9j6E1BeBQ4GFfWY",
            file=sys.stderr,
        )
        return 0
    if denied:
        print("\nsome decks were unreadable:", file=sys.stderr)
        for d in denied:
            print("  -", d, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(set(sys.argv[1:])))
