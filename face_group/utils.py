"""
Utils module
"""
import multiprocessing
import shutil
from itertools import repeat
from pathlib import Path
from typing import Any, List, Tuple
from typing import Optional

import numpy as np
from face_recognition import (face_distance, face_encodings, face_locations,
                              load_image_file)
from face_recognition.face_recognition_cli import image_files_in_folder
from rich.progress import track
from rich import print

IR_DIR = "ir"
RGB_DIR = "rgb"


def _copy_images_by_dict(
    faces_paths: List[List[Path]],
    input_dir: Path,
    output_dir: Path,
    verbose: bool=True,
):
    for num, img_paths in enumerate(faces_paths):
        path_rgb = output_dir / RGB_DIR / str(num)
        path_ir = output_dir / IR_DIR / str(num)

        if not path_rgb.exists():
            path_rgb.mkdir(parents=True)
        if not path_ir.exists():
            path_ir.mkdir(parents=True)

        for img_path in img_paths:
            rgb_name = img_path.name
            time = _get_timestamp(rgb_name)
            ir_name = f"infra_{time}.jpg"
            dst_rgb = path_rgb / rgb_name
            dst_ir = path_ir / ir_name
            shutil.copyfile(img_path, dst_rgb)
            try:
                shutil.copyfile(input_dir / IR_DIR / ir_name, dst_ir)
            except FileNotFoundError as error:
                if verbose:
                    print(error)


def _get_timestamp(name: str) -> str:
    return name.split("_")[-1].split(".")[0]


def _sort_path_by_encodings(
    np_face: np.ndarray, np_path: np.ndarray
) -> List[List[Path]]:
    """Сортирует пути по похожим энкодингам в словарь"""

    faces: List[List[Path]] = []
    while len(np_face) > 0:
        current, np_face = _np_pop(np_face)
        path, np_path = _np_pop(np_path)
        indexes = face_distance(np_face, current) <= 0.6
        faces.append(list(np_path[indexes]) + [path])
        np_face = np_face[~indexes]
        np_path = np_path[~indexes]
    return faces


def _np_pop(array: np.ndarray) -> Tuple[Any, np.ndarray]:
    """Операция pop для ndarray"""

    head = array[-1]
    tail = array[:-1]
    return head, tail


def _process_image(img_path, model="hog", verbose=True):
    image = load_image_file(img_path)
    face_bounding_boxes = face_locations(image, model=model)

    if len(face_bounding_boxes) != 1:
        # If there are no people (or too many people) in a training image,
        # skip the image.
        if verbose:
            print(
                "Image {} not suitable for training: {}".format(
                    img_path,
                    "Didn't find a face"
                    if len(face_bounding_boxes) < 1
                    else "Found more than one face",
                )
            )
    else:
        # Add face encoding for current image to list
        return face_encodings(image, known_face_locations=face_bounding_boxes)[0], Path(
            img_path
        )
    return None


def _get_encodings_from_image_dir(
    input_dir: Path, verbose: bool, model="hog", cpus: int = 1,
) -> Tuple[np.ndarray, np.ndarray]:
    """Извлекает энкодинги и возвращает вместе с путями"""

    images = image_files_in_folder(input_dir / RGB_DIR)

    if cpus == 1:
        results = _process_images_in_one_cpu(images, model, verbose)
    else:
        results = _process_images_in_process_pool(images, model, verbose, cpus)
    face_enc = [row[0] for row in results if row is not None]
    face_paths = [row[1] for row in results if row is not None]

    return np.array(face_enc), np.array(face_paths)


def _process_images_in_one_cpu(images, model, verbose):
    if verbose:
        results = [_process_image(image, model, verbose) for image in track(images,
                                                                            "Processing...")]
    else:
        results = [_process_image(image, model, verbose) for image in images]
    return results


def _process_images_in_process_pool(images, model, verbose, cpus):
    if cpus == -1:
        cpus = None
    pool = multiprocessing.Pool(cpus)
    function_parameters = zip(
        images,
        repeat(model),
        repeat(verbose),
    )
    if verbose:
        results = list(
            track(pool.imap(_process_image, images), "Processing...", total=len(images))
        )
    else:
        results = pool.starmap(_process_image, function_parameters)
    return results
