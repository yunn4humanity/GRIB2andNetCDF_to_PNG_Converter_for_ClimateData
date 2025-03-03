import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

def download_files(base_url, download_dir='downloads'):
    # 다운로드 디렉토리 생성
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    
    try:
        # 페이지 내용 가져오기
        response = requests.get(base_url)
        response.raise_for_status()  # 에러 체크
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # .gz로 끝나는 모든 링크 찾기
        for link in soup.find_all('a'):
            file_url = link.get('href')
            if file_url and file_url.endswith('.gz'):
                # 완전한 URL 만들기
                full_url = urljoin(base_url, file_url)
                file_name = os.path.basename(full_url)
                file_path = os.path.join(download_dir, file_name)
                
                try:
                    print(f'Downloading: {file_name}...')
                    # 파일 다운로드
                    file_response = requests.get(full_url, stream=True)
                    file_response.raise_for_status()
                    
                    # 파일 저장
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

# 사용 예시
if __name__ == "__main__":
    # 웹페이지 URL을 여기에 입력하세요
    base_url = "https://mrms.ncep.noaa.gov/2D/PrecipRate/"
    download_files(base_url)