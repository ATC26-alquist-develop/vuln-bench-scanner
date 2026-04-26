import subprocess
import os

def get_docker_images():
    """Get a list of all available Docker images."""
    try:
        output = subprocess.check_output(['docker', 'images', '--format', '{{.Repository}}:{{.Tag}}'])
        images = output.decode('utf-8').strip().split('\n')
        return images
    except subprocess.CalledProcessError as e:
        print(f"Error getting Docker images: {e}")
        return []

def select_docker_image(images):
    """Prompt the user to select a Docker image."""
    if not images:
        print("No Docker images found.")
        return None

    print("Available Docker images:")
    for i, image in enumerate(images, start=1):
        print(f"{i}. {image}")

    while True:
        try:
            choice = int(input("Enter the number of the image you want to use: "))
            if 1 <= choice <= len(images):
                return images[choice - 1]
            else:
                print("Invalid choice. Please enter a number between 1 and", len(images))
        except ValueError:
            print("Invalid input. Please enter a number.")

def run_docker_command(image, command):
    """Run a Docker command on the selected image."""
    try:
        subprocess.run(['docker', 'run', '-it', image, command], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")

def main():
    images = get_docker_images()
    if not images:
        print("No Docker images found. Please ensure Docker is installed and running.")
        return

    selected_image = select_docker_image(images)
    if selected_image:
        command = input("Enter the command you want to run inside the Docker container: ")
        run_docker_command(selected_image, command)

if __name__ == "__main__":
    main()