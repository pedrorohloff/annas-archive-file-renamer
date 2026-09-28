import argparse
import re
import shutil
from pathlib import Path

SEPARATOR = " -- "
EXTENSIONS = {".epub", ".mobi", ".azw3", ".pdf", ".djvu", ".fb2",
              ".cbz", ".cbr", ".txt", ".rtf", ".lit"}
INVALID_CHARS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')  # forbidden on Windows


def clean(text: str) -> str:
    """Replace characters that are invalid in filenames."""
    return INVALID_CHARS.sub("_", text).strip()


def build_new_name(path: Path) -> str:
    """Build the new filename as 'Title - Author.ext'."""
    ext = path.suffix.lower() if path.suffix.lower() in EXTENSIONS else ""
    stem = path.name[: -len(path.suffix)] if ext else path.name

    if SEPARATOR not in stem:
        return path.name

    parts = [p.strip() for p in stem.split(SEPARATOR)]
    title = clean(parts[0])
    author = clean(parts[1]) if len(parts) > 1 else ""

    base = f"{title} - {author}" if author else title
    return base + ext


def ask_for_folder() -> Path:
    """Ask the user for the folder containing the books until it is valid."""
    while True:
        raw = input("Enter the path to the folder containing your books: ").strip()
        raw = raw.strip("'\"")  # remove quotes added by drag-and-drop or copy/paste
        if not raw:
            print("Please enter a path.")
            continue

        folder = Path(raw).expanduser().resolve()
        if folder.is_dir():
            return folder
        print(f"Folder not found: {folder}")


def main():
    parser = argparse.ArgumentParser(
        description="Rename files downloaded from Anna's Archive.")
    parser.add_argument("source", nargs="?", type=Path,
                        help="folder containing the books (asked interactively if omitted)")
    parser.add_argument("--dry-run", action="store_true",
                        help="only show what would be done, without moving any file")
    args = parser.parse_args()

    if args.source is not None:
        source = args.source.expanduser().resolve()
        if not source.is_dir():
            raise SystemExit(f"Folder not found: {source}")
    else:
        source = ask_for_folder()

    target_dir = source / "formatted_books"
    if not args.dry_run:
        target_dir.mkdir(exist_ok=True)

    for old_path in sorted(source.iterdir()):
        if not old_path.is_file():
            continue

        new_name = build_new_name(old_path)
        new_path = target_dir / new_name

        if new_path.exists():
            print(f"Skipped (already exists): {new_name}")
            continue

        print(f"{old_path.name}\n   -> {new_name}")
        if not args.dry_run:
            shutil.move(str(old_path), str(new_path))

    print("Done.")


if __name__ == "__main__":
    main()
