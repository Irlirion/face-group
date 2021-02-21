"""
API module
"""

from pathlib import Path, PurePath
from typing import Optional
from typing import Union

from face_group.utils import (_copy_images_by_dict,
                              _get_encodings_from_image_dir,
                              _sort_path_by_encodings)


def process_images(
    input_dir: Union[str, PurePath],
    output_dir: Union[str, PurePath],
    verbose: bool = False,
    model: str = "hog",
    cpus: int = 1
) -> None:
    """Про"""
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    if not output_dir.exists():
        output_dir.mkdir()

    np_face, np_path = _get_encodings_from_image_dir(input_dir, verbose, model, cpus)

    face_dict = _sort_path_by_encodings(np_face, np_path)

    _copy_images_by_dict(face_dict, input_dir, output_dir, verbose)


if __name__ == "__main__":
    process_images("/home/irlirion/PycharmProjects/face-group/resources", "out")
