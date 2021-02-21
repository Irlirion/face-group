"""
Command line module
"""
import time
from typing import Optional

import click
from click import Choice, Path

from face_group.api import process_images


@click.command()
@click.option(
    "-i",
    "--input-dir",
    "input_dir",
    type=Path(exists=True),
    help="Path of directory with rgb and infra images.",
)
@click.option(
    "-o",
    "--output-dir",
    "output_dir",
    default="out",
    type=Path(),
    help="Path of output directory (default='out').",
)
@click.option(
    "-v", "--verbose", "verbose", default=True, type=bool, help="Show info or not."
)
@click.option(
    "-m",
    "--model",
    "model",
    default="hog",
    type=Choice(["hog", "cnn"]),
    help="Type of backend for computing features.",
)
@click.option(
    "-c",
    "--cpus",
    "cpus",
    default=1,
    type=int,
    help='Number of CPU cores to use in parallel (can speed up processing lots of '
         'images). -1 means "use all in system".',
)
def group_faces(input_dir: str, output_dir: str, verbose: bool, model: str, cpus: int) \
        -> None:
    """It groups the faces of similar people"""

    start = time.time()
    process_images(input_dir, output_dir, verbose, model, cpus)
    click.echo(f"Done in {time.time() - start}s")
