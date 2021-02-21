# Face group
> Grouping rgb and infra people`s faces by folders using face features

`face-group` finds faces using dlib

Parameters:
- *input-dir* - path of directory with rgb and infra images
- *output-dir* - path of output directory (default="out")
- *verbose* - show info or not
- *model* - type of backend for computing features

## Installation
```
sudo apt-get install build-essential cmake
pip install face-group
```
## Usage
```
$ face-group --help
Usage: face-group [OPTIONS]

  It groups the faces of similar people

Options:
  -i, --input-dir PATH   Path of directory with rgb and infra images.
  -o, --output-dir PATH  Path of output directory (default='out').
  -v, --verbose BOOLEAN  Show info or not.
  -m, --model [hog|cnn]  Type of backend for computing features.
  --help                 Show this message and exit.
```
