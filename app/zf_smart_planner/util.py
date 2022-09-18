from pathlib import Path


def load_static(name):
    static_dir: Optional[Path] = None
    for static_path in (search_dirs := [f"./{name}", f"../{name}", f"./app/{name}"]) :
        if (the_dir := Path(static_path)).exists():
            static_dir = the_dir
    if static_dir is None:
        raise IOError(f"Could not find static dir. Searched directories: {search_dirs}")

    return static_dir
