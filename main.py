import json
import re
import shutil

from datetime import datetime
from pathlib import Path
from typing import List, Tuple, Optional

import dateparser


LOG_FILE = Path("DELETE_LOG.txt")


def initialize_log() -> None:
    if LOG_FILE.exists():
        LOG_FILE.unlink()


def load_settings(settings_path: Path) -> dict:
    if not settings_path.exists():
        print(f"{settings_path.name} not found")
        exit(1)
        
    with settings_path.open('r', encoding='utf-8') as file:
        return json.load(file)


def parse_directory_date(name: str, folder_fmt: Optional[str]) -> Optional[datetime]:
    # Attempt to use the config format
    if folder_fmt:
        try:
            dt = datetime.strptime(name, folder_fmt)
            print(f"[DEBUG] CFG folder_format OK: '{name}' -> {dt} (format={folder_fmt})")
            return dt
        except ValueError as e:
            print(f"[DEBUG] CFG folder_format FAIL: '{name}' -> {e} (format={folder_fmt})")

    # Attempt numeric-only formats (where middle token is often the month)
    is_numeric_like = re.search(r"[A-Za-zА-Яа-я]", name) is None
    if is_numeric_like:
        numeric_date_formats = [
            '%Y-%m-%d', '%d-%m-%Y', '%Y_%m_%d', '%d_%m_%Y',
            '%Y.%m.%d', '%d.%m.%Y', '%Y %m %d', '%d %m %Y',
            '%d%m%Y', '%y-%m-%d', '%d-%m-%y', '%y_%m_%d', 
            '%d_%m_%y', '%y.%m.%d', '%d.%m.%y', '%y %m %d', '%d %m %y',
        ]
        dt = dateparser.parse(
            name,
            date_formats=numeric_date_formats,
            settings={
                'STRICT_PARSING': True,
                'RETURN_AS_TIMEZONE_AWARE': False,
                'PREFER_LOCALE_DATE_ORDER': False
            }
        )
        if dt:
            print(f"[DEBUG] NUMERIC Parse OK  : '{name}' -> {dt}")
            return dt
            
        print(f"[DEBUG] NUMERIC Parse FAIL (middle-is-month formats): '{name}'")

    # General fallback for non-numeric/mixed names
    dt = dateparser.parse(
        name,
        settings={
            'DATE_ORDER': 'DMY',
            'PREFER_DAY_OF_MONTH': 'first',
            'RETURN_AS_TIMEZONE_AWARE': False,
            'STRICT_PARSING': True
        }
    )
    
    if dt:
        print(f"[DEBUG] Parse OK  : '{name}' -> {dt}")
    else:
        print(f"[DEBUG] Parse FAIL: '{name}' -> None")
        
    return dt


def get_parsed_directories(folder_path: Path, folder_fmt: Optional[str]) -> List[Tuple[Path, datetime]]:
    print(f"[DEBUG] Entries in '{folder_path}'")
    parsed_dirs = []
    
    try:
        for item in folder_path.iterdir():
            if item.is_dir():
                dt = parse_directory_date(item.name, folder_fmt)
                if dt:
                    parsed_dirs.append((item, dt))
    except FileNotFoundError as e:
        print(f"[ERROR] {e}")
        
    return parsed_dirs


def enforce_retention_policy(parsed_dirs: List[Tuple[Path, datetime]], max_count: int) -> None:
    if not parsed_dirs:
        print("[DEBUG] No valid date-like directories recognized.")
        return

    parsed_dirs.sort(key=lambda t: t[1])
    
    debug_sorted = [f"{p.name} -> {d.isoformat()}" for p, d in parsed_dirs]
    print(f"[DEBUG] Sorted directories (oldest..newest) ({len(parsed_dirs)}): {debug_sorted}")

    while len(parsed_dirs) > max_count:
        oldest_path, oldest_dt = parsed_dirs.pop(0)
        print(f"[DEBUG] Deleting oldest: '{oldest_path.name}' ({oldest_dt}) -> {oldest_path}")
        
        shutil.rmtree(oldest_path, ignore_errors=True)
        
        with LOG_FILE.open('a', encoding='utf-8') as w:
            w.write(f"{datetime.now()} deleted folder: {oldest_path}\n")


def process_folder_group(folder_cfg: dict, index: int) -> None:
    folder_path = Path(folder_cfg["folder_path"])
    max_count = folder_cfg["folder_count"]
    folder_fmt = folder_cfg.get('folder_format')

    print(f"\n[DEBUG] Processing group #{index+1}: path='{folder_path}', limit={max_count}")
    
    parsed_dirs = get_parsed_directories(folder_path, folder_fmt)
    enforce_retention_policy(parsed_dirs, max_count)


def main() -> None:
    initialize_log()
    settings = load_settings(Path('settings.json'))

    for i, folder_cfg in enumerate(settings.get("folder", [])):
        process_folder_group(folder_cfg, i)


if __name__ == '__main__':
    main()
