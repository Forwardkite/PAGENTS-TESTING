import sys
import os

# Define the project root by going up three levels from the current directory
project_root = os.path.abspath('../../../')

# Define the path to the external tools and agents directories
tools_path = os.path.join(project_root, 'tools')
agents_path = os.path.join(project_root, 'agents')

# Print the paths to check if they are correct
print(f"Tools path: {tools_path}")
print(f"Agents path: {agents_path}")

# Add the directories to the Python path
sys.path.append(tools_path)
sys.path.append(agents_path)

# Print sys.path to ensure the directories are in the path
print(f"sys.path: {sys.path}")

# Now you can import from the tools and agents folders
try:
    from agents.user_proxy.user_proxy import get_user_proxy
    print("Successfully imported user_proxy.")
except ModuleNotFoundError as e:
    print(f"Import failed: {e}")
