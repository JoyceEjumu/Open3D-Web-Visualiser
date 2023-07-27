# Import necessary modules
from GUI_Functions import *
import random


# Function to handle different options based on the user's selection
def options(pcd):
    # get check box option ticked by user
    option = request.form.get('option')
    option1 = request.form.get('option1')
    option2 = request.form.get('option2')
    option3 = request.form.get('option3')
    option4 = request.form.get('option4')
    option5 = request.form.get('option5')
    option6 = request.form.get('option6')
    option7 = request.form.get('option7')
    option8 = request.form.get('option8')
    option9 = request.form.get('option9')
    option10 = request.form.get('option10')
    option11 = request.form.get('option11')

    # Perform operations based on the selected checkbox option
    if option:  # Visualiser
        # Open a new tab to visualize the point cloud
        open_tab()
        o3d.visualization.draw(pcd)

    elif option1:  # Voxel Down sampling
        # Down sample the point cloud using voxel down sampling
        open_tab()
        downpcd = pcd.voxel_down_sample(voxel_size=0.05)
        o3d.visualization.draw(downpcd)

    elif option2:  # Vertex Normal Estimation
        # Down sample the point cloud
        downpcd = pcd.voxel_down_sample(voxel_size=0.05)
        # Estimate vertex normals using KDTree search
        downpcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
        # Visualize the point cloud with vertex normals
        o3d.visualization.draw_geometries([downpcd],
                                          zoom=0.3412,
                                          front=[0.4257, -0.2125, -0.8795],
                                          lookat=[2.6172, 2.0475, 1.532],
                                          up=[-0.0694, -0.9768, 0.2024],
                                          point_show_normal=True)
    elif option3:  # Access Estimated Vertex Normal
        # Open a new tab with Flask app to get an integer input from the user
        url = "http://127.0.0.1:5000/enter_integer"
        threading.Thread(target=open_url, args=(url,)).start()
        option_3, integer = create_app(pcd)
        option_3.run()

    elif option4:  # Crop Point Cloud
        # Open a new tab with Flask app to upload a JSON file and crop the point cloud
        json_upload(4, pcd)

    elif option5:  # Paint Point Cloud
        # Paint the point cloud with a uniform color (orange in this case)
        pcd.paint_uniform_color([1, 0.706, 0])
        # Open a new tab to visualize the colored point cloud
        open_tab()
        o3d.visualization.draw(pcd)

    elif option6:  # Point Cloud Distance
        # Open a new tab with Flask app to upload a JSON file and calculate distances
        json_upload(6, pcd)
        # Display distances (distances are calculated in the json_options function)

    elif option7:  # Bounding Volumes
        # Open a new tab with Flask app to upload a JSON file and visualize bounding volumes
        json_upload(7, pcd)

    elif option8:  # Convex Hull
        # Estimate normals for the point cloud
        pcd.estimate_normals()
        # Estimate the radius for convex hull computation
        distances = pcd.compute_nearest_neighbor_distance()
        avg_dist = np.mean(distances)
        radius = 1.5 * avg_dist
        # Convert point cloud into a mesh using Ball Pivoting algorithm
        mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(pcd, o3d.utility.DoubleVector(
            [radius, radius * 2]))
        mesh.compute_vertex_normals()

        # Sample points for convex hull computation and visualize it
        pcl = mesh.sample_points_poisson_disk(number_of_points=2000)
        hull, _ = pcl.compute_convex_hull()
        hull_ls = o3d.geometry.LineSet.create_from_triangle_mesh(hull)
        hull_ls.paint_uniform_color((1, 0, 0))

        # Open a new tab to visualize the point cloud with convex hull
        open_tab()
        o3d.visualization.draw([pcl, hull_ls])

    elif option9:  # DBSCAN Clustering
        # Open a new tab with Flask app to enter DBSCAN clustering parameters
        url = "http://127.0.0.1:5000/enter_values"
        threading.Thread(target=open_url, args=(url,)).start()
        app9, eps_val, min_points_val = create_app_9(pcd)
        app9.run()

    elif option10:  # Planar Segmentation
        # Open a new tab with Flask app to enter planar segmentation parameters
        url = "http://127.0.0.1:5000/enter_segmentation_values"
        threading.Thread(target=open_url, args=(url,)).start()
        app10 = create_app10(pcd)
        app10.run()

    elif option11:  # Hidden Point Removal
        # Remove hidden points from the point cloud using a camera-based approach
        diameter = np.linalg.norm(np.asarray(pcd.get_max_bound()) - np.asarray(pcd.get_min_bound()))
        camera = [0, 0, diameter]
        radius = diameter * 100
        _, pt_map = pcd.hidden_point_removal(camera, radius)
        pcd = pcd.select_by_index(pt_map)

        # Open a new tab to visualize the point cloud after hidden point removal
        open_tab()
        o3d.visualization.draw(pcd)


# Function to open a new webpage
def open_webpage():
    webbrowser.open(url_main)


# Function to draw the point cloud
def draw_point_cloud(pcd):
    o3d.visualization.draw(pcd)


# Function to open a URL in a new browser tab
def open_url(url):
    webbrowser.open(url)


# Define Flask app and handle file uploads
@app.route('/', methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # upload .ply file
        uploaded_file = request.files['file']
        filename, basedir = process_file(uploaded_file)

        # Enable GUI backend for Webrtc server
        o3d.visualization.webrtc_server.enable_webrtc()
        basedir = app.config["IMAGE_UPLOADS"]
        file_path = os.path.join(basedir, filename)
        pcd = o3d.io.read_point_cloud(file_path)

        # Call options function for each check box option
        options(pcd)

    return render_template('main.html')


# Function to reload the main page
def reload_main_page():
    return render_template('main.html')


# Main function
if __name__ == '__main__':
    # Define a random port number
    port = 5000 + random.randint(0, 999)
    url_main = "http://127.0.0.1:{0}".format(port)

    # Open the webpage in a new tab
    threading.Thread(target=open_url, args=(url_main,)).start()
    # Run the Flask app on the defined port
    app.run(port=port, debug=False)
