# map-coloring
> Map coloring, using four colors

This program gets a map image as an input and produces all possible valid colorings of that map using backtracking.

The input image background and borders should be white.

# Algorithm

1. Detecting all non-white regions (eg. provinces or states).
2. Converting the input map to a simple planar graph:
There will be a node for each region. Two nodes will be adjacent, if and only if their correspondent region have a common border on the map.
3. Using backtracking for [coloring](https://en.wikipedia.org/wiki/Graph_coloring#Vertex_coloring) that graph (it's a recursive function that produces all valid colorings).
4. Displaying all produced colorings on the given map.

# Dependencies
Install numpy, matplotlib and opencv.

Linux:
```
sudo apt update
sudo apt upgrade
sudo apt install python3-numpy python3-scipy python3-matplotlib
sudo apt install python3-opencv
sudo apt install python3-pip
```

Windows (using pip3 is preferred):
```
pip install numpy
pip install scipy
pip install matplotlib
pip install opencv-python
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
It runs slowly on large images. It can be improved by changing the second part of its algorithm (setting the graph edges). Some computational geometry knowledge about polygons may be needed for this part.

Any contributions are welcomed.

