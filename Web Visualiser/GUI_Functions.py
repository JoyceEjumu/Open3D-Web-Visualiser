# Import necessary modules
from flask import Flask, request, render_template
import open3d as o3d
from werkzeug.utils import secure_filename
import numpy as np
import threading
import webbrowser
import os
import matplotlib.pyplot as plt
import html


# Function to open a URL in a new browser tab
def open_url(url):
    webbrowser.open(url)


# Function to create a Flask app and perform some operations on a point cloud (pcd)
def create_app(pcd):
    option_3 = Flask(__name__)
    integer = None
    # Down sample the point cloud using voxel down sampling
    downpcd = pcd.voxel_down_sample(voxel_size=0.05)

    @option_3.route('/enter_integer', methods=['GET', 'POST'])
    def enter_integer():
        nonlocal integer
        if request.method == 'POST':
            # Get the integer value from the form input
            integer = int(request.form.get('integer'))
            # Get the first 'integer' number of normals as a list
            list_vals = np.asarray(downpcd.normals)[:integer]
            # Convert the list to a formatted string with line breaks for display
            list_str = '\n'.join(map(str, list_vals))
            formatted_list_str = '<pre>{}</pre>'.format(html.escape(list_str).replace('\n', '<br>'))
            # Render the template with the integer value and the formatted list
            return render_template('display_integer.html', integer=integer, list_vals=formatted_list_str)
        return render_template('enter_integer.html')

    return option_3, integer


# Function to open a URL in a new thread, used to open Flask app in a new tab
def open_tab():
    url = "http://localhost:8888"
    threading.Thread(target=open_url, args=(url,)).start()


# Define Flask app for image uploads
app = Flask(__name__)

# Define allowed extensions for image uploads
app.config["IMAGE_UPLOADS"] = "static/Images"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PLY"]


# Function to create a Flask app and handle option 2
def create_app_2():
    @app.route('/option2', methods=['GET', 'POST'])
    def option2():
        if request.method == 'POST':
            # Get the integer value from the form input
            integer = request.form.get('integer')
            # Render the template with the integer value
            return render_template('display_integer.html', integer=integer)
        return render_template('enter_integer.html')


# Function to perform DBSCAN clustering on the point cloud
# Function to perform DBSCAN clustering on the point cloud
def dbscan(pcd, eps, min_points):
    with o3d.utility.VerbosityContextManager(
            o3d.utility.VerbosityLevel.Debug) as cm:
        # Cluster points using DBSCAN algorithm
        labels = np.array(
            pcd.cluster_dbscan(eps=eps, min_points=min_points, print_progress=True))

    max_label = labels.max()
    print(f"point cloud has {max_label + 1} clusters")
    # Color the point cloud based on the clusters
    colors = plt.get_cmap("tab20")(labels / (max_label if max_label > 0 else 1))
    colors[labels < 0] = 0
    pcd.colors = o3d.utility.Vector3dVector(colors[:, :3])
    # Open Flask app in a new tab to visualize the clustered point cloud
    open_tab()
    o3d.visualization.draw(pcd)


def create_app_9(pcd):
    option_9 = Flask(__name__)
    eps_val = None
    min_points_val = None

    @option_9.route('/enter_values', methods=['GET', 'POST'])
    def enter_values():
        nonlocal eps_val, min_points_val
        if request.method == 'POST':
            # Get the float and integer values from the form input
            eps_val = float(request.form.get('float1'))
            min_points_val = int(request.form.get('integer2'))
            # Perform DBSCAN clustering using the entered values
            dbscan(pcd, eps_val, min_points_val)

        return render_template('enter_values.html')

    return option_9, eps_val, min_points_val


# Function to create a Flask app and handle option 10
def create_app10(pcd):
    option_10 = Flask(__name__)
    dist_thresh = None
    ransac = None
    no_iterations = None

    @option_10.route('/enter_segmentation_values', methods=['GET', 'POST'])
    def enter_values():
        nonlocal dist_thresh, ransac, no_iterations
        if request.method == 'POST':
            # Get the float and integer values from the form input
            dist_thresh = float(request.form.get('float1'))
            ransac = int(request.form.get('integer2'))
            no_iterations = int(request.form.get('integer3'))

            # Segment the point cloud using RANSAC plane fitting
            plane_model, inliers = pcd.segment_plane(distance_threshold=dist_thresh,
                                                     ransac_n=ransac,
                                                     num_iterations=no_iterations)
            [a, b, c, d] = plane_model
            print(f"Plane equation: {a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0")

            # Color the inliers (plane) in red and the outliers in blue
            inlier_cloud = pcd.select_by_index(inliers)
            inlier_cloud.paint_uniform_color([1.0, 0, 0])
            outlier_cloud = pcd.select_by_index(inliers, invert=True)
            # Open Flask app in a new tab to visualize the segmented point cloud
            open_tab()
            o3d.visualization.draw([inlier_cloud, outlier_cloud])
        return render_template('enter_seg_values.html')

    return option_10


def process_file(file):
    # process ply file
    if file.filename == '':
        print("File must have a name")

    # define path to uploaded ply file
    filename = secure_filename(file.filename)
    basedir = os.path.abspath(os.path.dirname(__file__))
    file.save(os.path.join(basedir, app.config["IMAGE_UPLOADS"], filename))
    return filename, basedir


# Function to process uploaded JSON files
def process_file_json(file, app):
    # process .json file
    if file.filename == '':
        print("File must have a name")

    # define path to uploaded .json file
    filename = secure_filename(file.filename)
    basedir = os.path.abspath(os.path.dirname(__file__))
    file.save(os.path.join(basedir, app.config["IMAGE_UPLOADS"], filename))
    return filename, basedir


# Function to upload and handle JSON files for different options
def json_upload(option_no, pcd):
    # define Flask app
    app_json = Flask(__name__)

    # define allowed extensions
    app_json.config["IMAGE_UPLOADS"] = "static/Images"
    app_json.config["ALLOWED_IMAGE_EXTENSIONS"] = ["json"]

    @app_json.route('/json_upload', methods=["GET", "POST"])
    def upload_file():
        filename = None  # Initialize filename variable

        if request.method == "POST":
            # upload .json file
            uploaded_file = request.files['file']
            filename, basedir = process_file_json(uploaded_file, app_json)

            # enable GUI backend
            basedir = app_json.config["IMAGE_UPLOADS"]
            file_path = os.path.join(basedir, filename)
            json_options(option_no, pcd, file_path)

        return render_template('main_json_upload.html', filename=filename)

    # define port
    url_main = "http://127.0.0.1:5000/json_upload"
    # open webpage
    threading.Thread(target=open_url, args=(url_main,)).start()
    app_json.run(port=5000, debug=False)


def json_options(option, pcd, json_path):
    if option == 4:
        print("option 4")
        vol = o3d.visualization.read_selection_polygon_volume(json_path)
        crop = vol.crop_point_cloud(pcd)
        open_tab()
        o3d.visualization.draw(crop)

    elif option == 6:
        print("option 6")

        point_cloud_1 = pcd  # pcd
        vol = o3d.visualization.read_selection_polygon_volume(json_path)
        point_cloud_2 = vol.crop_point_cloud(point_cloud_1)  # crop

        dists = point_cloud_1.compute_point_cloud_distance(point_cloud_2)
        dists = np.asarray(dists)
        ind = np.where(dists > 0.01)[0]
        pcd_after_crop = point_cloud_1.select_by_index(ind)

        pcd_after_crop.paint_uniform_color([0, 0, 1])
        point_cloud_2.paint_uniform_color([0.5, 0.5, 0])

        print(dists)

        open_tab()
        o3d.visualization.draw([pcd_after_crop, point_cloud_2])

    elif option == 7:
        print("option 7")
        # demo_crop_data = o3d.data.DemoCropPointCloud()
        vol = o3d.visualization.read_selection_polygon_volume(json_path)
        crop = vol.crop_point_cloud(pcd)
        aabb = crop.get_axis_aligned_bounding_box()
        aabb.color = (1, 0, 0)
        obb = crop.get_oriented_bounding_box()
        obb.color = (0, 1, 0)

        open_tab()
        o3d.visualization.draw([crop, aabb, obb])
