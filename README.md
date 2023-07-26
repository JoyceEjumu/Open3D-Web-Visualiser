# Open3D-Web-Visualiser
A web visualiser that uses Open3D to inspect and view assets over a wireless network.

## Dependencies
+ open3d
  + and its various dependencies
+ Flask

## Setup 


### Installing Using Pip
    pip install open3d
    pip install Flask

# Wireless Transfer
To transfer files between two devices over a wireless network, you will need to run the wireless transfer file on the server. Once run, there will be an HTTP link in the terminal. Enter this link into your client's browser. This will open a webpage which will display all the files in the specific directory, making them available for download. 

# Web Visualiser

## Loading in Point Clouds
When the Web Visualiser is run, it shall open a webpage which allows you to upload a .ply file. Once done, you may choose the option below to view or process the file. 

  
The Web Visualiser has the following functions:
- Visualize point cloud
- Voxel downsampling
- Vertex normal estimation
- Access estimated vertex normal
- Crop point cloud
- Paint point cloud
- Point cloud distance
- Bounding volumes
- Convex hull
- DBSCAN clustering
- Plane segmentation
- Planar patch detection
- Hidden point removal


### Visualize point cloud
This option reads and visualises a point cloud. The functions used include: 
- read_point_cloud: which reads a point cloud from a file. 
- draw_geometries: which visualises the point cloud.

#### Voxel downsampling
Creates a uniformly downsampled point cloud from an input cloud. This is done by bucketing points into voxels and generating an average for all points inside a voxel.

### Vertex normal estimation
Computes the normal for each point. The function finds adjacent points and calculates the principal axis using covariance analysis. 

### Access estimated vertex normal
This function will open a webpage, prompting the user to enter the number of normal points they want to be displayed. Once entered, a new webpage will open displaying the requested number of normal points. 

### Crop point cloud

### Paint point cloud

### Point cloud distance

### Bounding volumes

### Convex hull

### DBSCAN clustering

### Plane segmentation

### Planar patch detection

### Hidden point removal

