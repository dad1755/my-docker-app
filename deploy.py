import subprocess
import os

def deploy_app(app_folder, url_path, port):
    try:
        # Ensure the app_folder is an absolute path
        app_folder = os.path.abspath(app_folder)

        # Use the folder name as the image name (without path)
        image_name = os.path.basename(app_folder)

        # Build the Docker image from the Dockerfile located in the app_folder
        build_command = ["docker", "build", "-t", image_name, app_folder]
        print(f"Building Docker image: {' '.join(build_command)}")
        subprocess.run(build_command, check=True)

        # Now run the container
        run_command = [
            "docker", "run",
            "-d",  # Run container in detached mode
            "-p", f"{port}:8501",  # Map the host port to the container port
            image_name  # Use the built image name
        ]

        print(f"Running Docker container: {' '.join(run_command)}")
        subprocess.run(run_command, check=True)

        # If the command was successful, return True
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error deploying app: {e}")  # Log the error for debugging
        return False
