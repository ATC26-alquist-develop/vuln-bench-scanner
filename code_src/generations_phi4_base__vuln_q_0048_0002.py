import subprocess

def run_docker_command(image_name):
    try:
        subprocess.run(['docker', 'run', image_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

def main():
    image_name = input("Enter the Docker image name: ")
    run_docker_command(image_name)

if __name__ == "__main__":
    main()