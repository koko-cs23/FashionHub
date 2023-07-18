from pyuploadcare import Uploadcare, ProjectInfo
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve Uploadcare API keys from environment variables
uploadcare_public_key = os.getenv('UPLOADCARE_PUBLIC_KEY')
uploadcare_secret_key = os.getenv('UPLOADCARE_SECRET_KEY')

# access api
uploadcare = Uploadcare(uploadcare_public_key, uploadcare_secret_key)

def get_uploaded_image_urls():
    files = uploadcare.list_files(stored=True)
    image_urls = [file.info['original_file_url'] for file in files]

    return image_urls

def save_image_urls():
    files = uploadcare.list_files(stored=True)
    image_urls = [file.info['original_file_url'] for file in files]

    with open('index.txt', 'w') as file:
        file.writelines(image_url + '\n' for image_url in image_urls)

def getProjectInfo():
    project_info = uploadcare.get_project_info()

    print(project_info)

getProjectInfo()
#save_image_urls()
