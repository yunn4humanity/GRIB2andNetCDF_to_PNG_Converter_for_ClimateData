import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

def download_files(base_url, download_dir='downloads'):
    # Create download directory
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    
    try:
        # Get page content
        response = requests.get(base_url)
        response.raise_for_status()  # Check for errors
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all links ending with .gz
        for link in soup.find_all('a'):
            file_url = link.get('href')
            if file_url and file_url.endswith('.gz'):
                # Create complete URL
                full_url = urljoin(base_url, file_url)
                file_name = os.path.basename(full_url)
                file_path = os.path.join(download_dir, file_name)
                
                try:
                    print(f'Downloading: {file_name}...')
                    # Download file
                    file_response = requests.get(full_url, stream=True)
                    file_response.raise_for_status()
                    
                    # Save file
                    with open(file_path, 'wb') as f:
                        for chunk in file_response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                    
                    print(f'Successfully downloaded: {file_name}')
                
                except Exception as e:
                    print(f'Error downloading {file_name}: {str(e)}')
                    continue
        
        print('\nAll downloads completed!')
        
    except Exception as e:
        print(f'Error accessing the page: {str(e)}')

# Usage example
if __name__ == "__main__":
    # Enter the webpage URL here
    base_url = "https://mrms.ncep.noaa.gov/2D/PrecipRate/"
    download_files(base_url)