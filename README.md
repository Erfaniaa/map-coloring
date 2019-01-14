# map-coloring
> Map coloring, using four colors

This program gets a map image as an input and produces all possible colorings of that map using backtracking.

The input image background and borders should be white.

# Dependencies
Install numpy, matplotlib and opencv.
```
sudo apt update
sudo apt upgrade
sudo apt install python3-numpy python3-scipy python3-matplotlib
sudo apt install python3-opencv
sudo apt install python3-pip
```

# Run
```
python3 map_coloring.py map_image_file_name
```

# Samples
```
python3 map_coloring.py iran.jpg
```
The original image:

<img src="https://user-images.githubusercontent.com/7780269/51145922-88122000-186a-11e9-9577-b4b33f767731.jpg" width="300">

A part of the program output:

<img src="https://user-images.githubusercontent.com/7780269/51145956-9eb87700-186a-11e9-9eaf-fce66e7b5b6b.gif" width="300">

```
python3 map_coloring.py tehran_province.jpg
```
The original image:

<img src="https://user-images.githubusercontent.com/7780269/51145925-88122000-186a-11e9-81a5-c3c633496866.jpg" width="300">

A part of the program output:

<img src="https://user-images.githubusercontent.com/7780269/51145952-9e1fe080-186a-11e9-8968-09861c3a7008.gif" width="300">

```
python3 map_coloring.py usa.png
```
The original image:

<img src="https://user-images.githubusercontent.com/7780269/51146422-028f6f80-186c-11e9-941c-c77f332c81b4.png" width="300">

A part of the program output:

<img src="https://user-images.githubusercontent.com/7780269/51145955-9e1fe080-186a-11e9-9cf2-96fc1a9198f7.gif" width="300">

# Notes
It runs slowly on large images.

