# map-coloring
> Map coloring, using four colors

This program gets a map image as an input and produce all possible colorings of that map using backtracking.

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
Original Image:

![iran](https://user-images.githubusercontent.com/7780269/51145922-88122000-186a-11e9-9577-b4b33f767731.jpg)

Program output:

![iran_output](https://user-images.githubusercontent.com/7780269/51145956-9eb87700-186a-11e9-9eaf-fce66e7b5b6b.gif)

```
python3 map_coloring.py tehran_province.jpg
```
Original Image:

![tehran_province](https://user-images.githubusercontent.com/7780269/51145925-88122000-186a-11e9-81a5-c3c633496866.jpg)

Program output:

![tehran_province_output](https://user-images.githubusercontent.com/7780269/51145952-9e1fe080-186a-11e9-8968-09861c3a7008.gif)

```
python3 map_coloring.py usa.png
```

Original Image:

![usa](https://user-images.githubusercontent.com/7780269/51146221-78470b80-186b-11e9-9db3-8a9701d2d0c3.png)


Program output:

![usa_output](https://user-images.githubusercontent.com/7780269/51145955-9e1fe080-186a-11e9-9cf2-96fc1a9198f7.gif)

# Notes
It runs slowly on large images.

