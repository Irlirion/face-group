# Face group
> Grouping rgb and infra people`s faces by folders using face features

`face-group` finds faces using dlib


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
  -c, --cpus INTEGER     Number of CPU cores to use in parallel (can speed up
                         processing lots of images). -1 means "use all in
                         system".

  --help                 Show this message and exit.
```
