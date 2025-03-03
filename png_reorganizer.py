import os
import shutil
from collections import defaultdict

def reorganize_radar_files(source_dir, target_dir, frames_per_case=29):
    """
    레이더 PNG 파일들을 재구성하는 함수 - 각 시점의 가장 낮은 sweep만 선택
    
    Parameters:
    source_dir (str): 원본 PNG 파일들이 있는 디렉토리
    target_dir (str): 재구성된 파일들을 저장할 디렉토리
    frames_per_case (int): 각 케이스(폴더)당 필요한 프레임 수
    """
    print(f"Starting file reorganization...")
    print(f"Source directory: {source_dir}")
    print(f"Target directory: {target_dir}")
    
    os.makedirs(target_dir, exist_ok=True)
    
    # 시점별로 파일들을 그룹화
    time_groups = defaultdict(list)
    
    # 모든 PNG 파일 수집 및 그룹화
    total_files_found = 0
    print("\nScanning for PNG files...")
    
    for root, _, files in os.walk(source_dir):
        png_files = [f for f in files if f.endswith('.png')]
        print(f"Found {len(png_files)} PNG files in this directory")
        
        for file in png_files:
            total_files_found += 1
            # 파일 이름 파싱 (예: RDR_SSP_FQC_202501081335_sweep_1.png)
            parts = file.split('_')
            if len(parts) >= 6:
                try:
                    time_point = parts[3]  # 시간 정보 (예: 202501081335)
                    sweep_num = int(parts[5].split('.')[0])  # sweep 번호
                    full_path = os.path.join(root, file)
                    time_groups[time_point].append((sweep_num, full_path))
                    print(f"Processed: {file} (time_point: {time_point}, sweep: {sweep_num})")
                except (ValueError, IndexError) as e:
                    print(f"Error processing file {file}: {str(e)}")
            else:
                print(f"Skipping file with unexpected format: {file}")
    
    print(f"\nTotal PNG files found: {total_files_found}")
    print(f"Unique time points found: {len(time_groups)}")
    
    # 각 시점별로 가장 낮은 sweep만 선택
    lowest_sweep_files = []
    print("\nSelecting lowest sweeps for each time point...")
    
    for time_point in sorted(time_groups.keys()):
        files = time_groups[time_point]
        if files:
            # sweep 번호로 정렬하고 가장 낮은 것 선택
            files.sort(key=lambda x: x[0])
            lowest_sweep_files.append((time_point, files[0][1]))
            print(f"Time point {time_point}: Selected sweep {files[0][0]}")
    
    print(f"\nTotal lowest sweep files selected: {len(lowest_sweep_files)}")
    
    # 선택된 파일들을 29개씩 묶어서 케이스로 구성
    total_cases = len(lowest_sweep_files) // frames_per_case
    print(f"\nTotal number of complete cases that can be created: {total_cases}")
    
    if total_cases == 0:
        print("\nNot enough files to create complete cases!")
        print(f"Need {frames_per_case} files per case, but only found {len(lowest_sweep_files)} files")
        return
    
    # 각 케이스별로 처리
    for case_idx in range(total_cases):
        case_id = str(case_idx).zfill(5)
        case_dir = os.path.join(target_dir, case_id)
        os.makedirs(case_dir, exist_ok=True)
        
        print(f"\nProcessing case {case_id}...")
        
        # 이 케이스에 해당하는 29개 파일 복사
        for frame_idx in range(frames_per_case):
            file_idx = case_idx * frames_per_case + frame_idx
            if file_idx < len(lowest_sweep_files):
                _, source_file = lowest_sweep_files[file_idx]
                new_filename = f"{case_id}-{str(frame_idx).zfill(2)}.png"
                target_file = os.path.join(case_dir, new_filename)
                
                # 파일 복사
                shutil.copy2(source_file, target_file)
                print(f"Copied: {new_filename}")
            else:
                print(f"Warning: Not enough source files for case {case_id}, frame {frame_idx}")
                break

if __name__ == "__main__":
    # 사용 예시
    source_directory = "D:/GLP/Korea_Climate_Data/KoreanPngDataset"  # 원본 PNG 파일들이 있는 디렉토리
    target_directory = "D:/GLP/Korea_Climate_Data/ReorganizedDataset"  # 재구성된 파일들을 저장할 디렉토리
    
    reorganize_radar_files(source_directory, target_directory)
    print("\nFile reorganization complete!")