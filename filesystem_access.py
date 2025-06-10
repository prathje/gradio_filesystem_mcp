import os
import shutil
import re
import difflib
from pathlib import Path
from typing import List, Dict, Union
import fnmatch

class FilesystemAccess:
    def __init__(self, root_path: str):
        self.root = Path(root_path).resolve()
        if not self.root.is_dir():
            raise ValueError("Root path must be an existing directory.")

    def _resolve_path(self, path: str) -> Path:
        full_path = (self.root / path).resolve()
        if not str(full_path).startswith(str(self.root)):
            raise PermissionError("Access outside root path is not allowed.")
        return full_path

    def read_file(self, path: str) -> str:
        full_path = self._resolve_path(path)
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return "Could not read file"

    def read_multiple_files(self, paths: List[str]) -> Dict[str, Union[str, Exception]]:
        results = {}
        for path in paths:
            results[path] = self.read_file(path)
        return results

    def write_file(self, path: str, content: str):
        full_path = self._resolve_path(path)
        full_path.parent.mkdir(parents=True, exist_ok=True)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def create_directory(self, path: str):
        full_path = self._resolve_path(path)
        full_path.mkdir(parents=True, exist_ok=True)

    def list_directory(self, path: str) -> List[str]:
        full_path = self._resolve_path(path)
        if not full_path.is_dir():
            raise NotADirectoryError("Path is not a directory.")
        return  [("[D] " if p.is_dir() else "[F] ") + p.name for p in full_path.iterdir()]

    def move_file(self, source: str, destination: str):
        src_path = self._resolve_path(source)
        dst_path = self._resolve_path(destination)
        dst_path.parent.mkdir(parents=True, exist_ok=True)

        if dst_path.exists():
            raise FileExistsError("Destination already exists.")
        shutil.move(str(src_path), str(dst_path))

    def search_files(self, path: str, pattern: str, excludePatterns: List[str]) -> List[str]:
        start_path = self._resolve_path(path)
        matches = []

        for root, dirs, files in os.walk(start_path):
            for name in dirs + files:
                full_path = Path(root) / name
                rel_path = full_path.relative_to(self.root)
                str_path = str(rel_path)

                if fnmatch.fnmatchcase(name.lower(), pattern.lower()):
                    if not any(fnmatch.fnmatchcase(str_path, excl) for excl in excludePatterns):
                        matches.append(str(rel_path))

        return matches

    def directory_tree(self, path: str) -> str:
        full_path = self._resolve_path(path)
        return "\n".join(self._directory_subtree(full_path))

    def _directory_subtree(self, path: Path) -> List[str]:
        tree = []
        for item in path.iterdir():
            if item.is_dir():
                tree.append(f"[D] {item.name}")
                subtree = self._directory_subtree(item.resolve())
                for line in subtree:
                    tree.append("   " + line)
            else:
                tree.append(f"[F] {item.name}")
        return tree