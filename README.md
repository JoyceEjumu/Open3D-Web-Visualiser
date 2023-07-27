# Open3D Web Visualiser

Welcome to Open3D Web Visualiser, a highly interactive tool that leverages Open3D to inspect and view 3D assets across a wireless network.

## Dependencies

Our application primarily depends on the following Python packages:

- open3d
- Flask

## Setup 

### Installing with Pip

You can quickly install the necessary dependencies using pip:

```
pip install open3d
pip install Flask
```

## Wireless Transfer

Our application supports wireless file transfer between two devices over a network. To do this:

1. Run the wireless transfer file on the server device.
2. A link will be displayed in the terminal.
3. Input this link into your client device's browser.
4. The webpage that opens will display all files available for download from the server's specified directory.

Please note that the path from which files are to be downloaded must be specified in the Wireless Transfer Code.

## Web Visualiser

### Loading Point Clouds

Run the Web Visualiser, which opens a webpage with an option to upload a .ply file. After upload, you can choose various options to view or process the file.

The Web Visualiser supports these operations:

- Visualise point cloud
- Perform voxel downsampling
- Estimate vertex normal
- Access estimated vertex normal
- Crop point cloud
- Paint point cloud
- Compute point cloud distance
- Generate bounding volumes
- Construct convex hull
- Perform DBSCAN clustering
- Execute plane segmentation
- Detect planar patches
- Remove hidden points

The above functions are built using Open3D, and the details of each operation are provided below:

#### Visualise Point Cloud

This option allows you to load and visualize a point cloud from a file.

#### Voxel Downsampling

It creates a uniformly downsampled point cloud from the input cloud using a grid of voxels.

#### Vertex Normal Estimation

This computes the normal for each point in the point cloud by considering its neighbouring points.

#### Access Estimated Vertex Normal

Displays a user-defined number of estimated vertex normals from the point cloud.

#### Crop Point Cloud

Allows you to upload a .json file that specifies a polygon selection area for cropping the point cloud.

#### Paint Point Cloud

Paints the entire point cloud with a uniform colour.

#### Point Cloud Distance

Allows you to upload a .json file that specifies a polygon selection area for cropping the point cloud, then computes the distance from each point in the source point cloud to the closest point in the cropped point cloud.

#### Bounding Volumes

Identifies and displays the bounding volume of a selected portion of the point cloud.

#### Convex Hull

Computes and visualizes the smallest convex set that contains all the points in the point cloud.

#### DBSCAN Clustering

Implements the DBSCAN clustering algorithm to group local clusters in the point cloud together.

#### Plane Segmentation

Identifies the largest planar segment in the point cloud using the RANSAC algorithm.

#### Hidden Point Removal

Removes any hidden (background) points to enhance the clarity of the point cloud.



#### Enjoy exploring the features of our Open3D Web Visualiser!
