import streamlit as st
from folder_manager import manage_folders
from deploy import deploy_app

# App Title
st.title("Local App Deployment Platform")

# Global variable to store deployed apps and used ports
deployed_apps = []
used_ports = []

# Function to get the next available port
def get_next_available_port(used_ports):
    base_port = 8501
    while base_port in used_ports:
        base_port += 1
    return base_port

# Step 1: Create 3 columns on the main page
col1, col2, col3 = st.columns(3)

# ---- Column 1: List of Deployed Apps ----
with col1:
    st.header("Deployed Apps")
    if deployed_apps:
        for app in deployed_apps:
            st.write(f"- {app['folder']} deployed at {app['url']}")
    else:
        st.write("No apps deployed yet.")

# ---- Column 2: Folder Management ----
with col2:
    created_folders = manage_folders()  # Get created folders from the manager

# ---- Column 3: App Deployment Settings ----
with col3:
    st.header("Deployment Settings")
    app_folder = st.selectbox("Select App Folder:", options=created_folders)

    url_path = st.text_input("Enter the URL path for the app (e.g., /app1):")

    if st.button("Deploy App"):
        st.write("Deploy button clicked.")  # Debug statement
        if app_folder and url_path:
            # Find the next available port
            port = get_next_available_port(used_ports)
            st.write(f"Attempting to deploy on port {port}.")  # Debug statement
            result = deploy_app(app_folder, url_path, port)  # Pass port to deploy_app function

            # Check the result of deployment
            if result:
                # Create a dictionary for the deployed app details
                deployed_apps.append({
                    'folder': app_folder,
                    'url': f"http://localhost:{port}{url_path}"
                })
                used_ports.append(port)  # Track the used port
                st.success(f"App '{app_folder}' successfully deployed at http://localhost:{port}{url_path}")
            else:
                st.error("Failed to deploy the app. Check the logs.")
        else:
            st.error("Please provide both the app folder and URL path.")
