import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import os
import glob
import zipfile
from datetime import datetime
import traceback

def radar_to_cartesian(file_path, output_dir, variable='DBZH'):
    """
    레이더 데이터를 카테시안 좌표계로 변환하여 PNG로 저장
    
    Parameters:
    file_path (str): NC 파일 경로
    output_dir (str): PNG 파일 저장 경로
    variable (str): 변환할 변수명
    
    Returns:
    list: 생성된 PNG 파일들의 경로 리스트
    """
    generated_files = []
    try:
        print(f"\nProcessing file: {file_path}")
        ds = xr.open_dataset(file_path)
        
        # 데이터셋 구조 확인
        print(f"Dataset variables: {list(ds.variables.keys())}")
        print(f"Dataset dimensions: {ds.dims}")
        
        # variable이 존재하는지 확인
        if variable not in ds.variables:
            print(f"Warning: Variable '{variable}' not found in dataset. Available variables: {list(ds.variables.keys())}")
            return generated_files
        
        # sweep_start_ray_index가 존재하는지 확인
        if 'sweep_start_ray_index' not in ds.variables:
            print("Warning: 'sweep_start_ray_index' not found in dataset")
            return generated_files
            
        base_filename = os.path.splitext(os.path.basename(file_path))[0]
        
        print(f"Number of sweeps: {len(ds.sweep_start_ray_index)}")
        
        for sweep_idx in range(len(ds.sweep_start_ray_index)):
            try:
                start_idx = ds.sweep_start_ray_index[sweep_idx].values
                end_idx = ds.sweep_end_ray_index[sweep_idx].values
                
                print(f"Processing sweep {sweep_idx}: start_idx={start_idx}, end_idx={end_idx}")
                
                start_gate_idx = start_idx * len(ds['range'])
                end_gate_idx = (end_idx + 1) * len(ds['range'])
                sweep_data = ds[variable].values[start_gate_idx:end_gate_idx].reshape(-1, len(ds['range']))
                
                print(f"Sweep data shape: {sweep_data.shape}")
                
                if sweep_data.size > 0:
                    azimuths = np.radians(ds.azimuth[start_idx:end_idx+1].values)
                    ranges = ds.range.values
                    
                    r, az = np.meshgrid(ranges, azimuths[:sweep_data.shape[0]])
                    
                    x = r * np.sin(az)
                    y = r * np.cos(az)
                    
                    fig = plt.figure(figsize=(10, 10), facecolor='black')
                    ax = plt.axes(facecolor='black')
                    
                    mesh = ax.pcolormesh(x/1000, y/1000, sweep_data,
                                       cmap='Greys_r',
                                       vmin=-20,
                                       vmax=80)
                    
                    ax.set_aspect('equal')
                    ax.set_xticks([])
                    ax.set_yticks([])
                    ax.set_xticklabels([])
                    ax.set_yticklabels([])
                    plt.axis('off')
                    
                    plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
                    plt.margins(0,0)
                    
                    output_filename = f'{base_filename}_sweep_{sweep_idx}.png'
                    output_path = os.path.join(output_dir, output_filename)
                    
                    plt.savefig(output_path,
                               bbox_inches='tight',
                               pad_inches=0,
                               dpi=300,
                               facecolor='black',
                               edgecolor='none')
                    plt.close()
                    
                    generated_files.append(output_path)
                    print(f"Generated: {output_path}")
                else:
                    print(f"Warning: Empty sweep data for sweep {sweep_idx}")
                    
            except Exception as sweep_error:
                print(f"Error processing sweep {sweep_idx}: {str(sweep_error)}")
                print(traceback.format_exc())
                continue
                
        ds.close()
        return generated_files
    
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        print(traceback.format_exc())
        return generated_files

def process_radar_files(input_dir, output_dir, zip_path):
    """
    지정된 디렉토리의 모든 NC 파일을 처리하고 결과를 ZIP으로 압축
    
    Parameters:
    input_dir (str): NC 파일이 있는 디렉토리 경로
    output_dir (str): PNG 파일을 저장할 디렉토리 경로
    zip_path (str): 최종 ZIP 파일 경로
    """
    os.makedirs(output_dir, exist_ok=True)
    
    nc_files = glob.glob(os.path.join(input_dir, "*.nc"))
    print(f"Found {len(nc_files)} NC files")
    
    all_generated_files = []
    
    for i, nc_file in enumerate(nc_files, 1):
        print(f"\nProcessing file {i}/{len(nc_files)}: {nc_file}")
        try:
            generated_files = radar_to_cartesian(nc_file, output_dir)
            all_generated_files.extend(generated_files)
        except Exception as e:
            print(f"Failed to process {nc_file}: {str(e)}")
            print(traceback.format_exc())
            continue
    
    if all_generated_files:
        print(f"\nCreating ZIP file at {zip_path}...")
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in all_generated_files:
                arcname = os.path.relpath(file, output_dir)
                zipf.write(file, arcname)
        print("ZIP file created successfully")
    else:
        print("\nNo PNG files were generated, skipping ZIP creation")
    
    print(f"\nProcessing complete.")
    print(f"Total files processed: {len(nc_files)}")
    print(f"Total PNG files generated: {len(all_generated_files)}")
    print(f"ZIP file created at: {zip_path}")

# 사용 예시
if __name__ == "__main__":
    input_directory = "D:\GLP\Korea_Climate_Data\extracted_netcdf"  # NC 파일이 있는 디렉토리
    output_directory = "D:\GLP\Korea_Climate_Data\KoreanPngDataset"  # PNG 파일을 저장할 디렉토리
    zip_file_path = "D:\GLP\Korea_Climate_Data/KoreaClimateDataset.zip"  # 최종 ZIP 파일 경로
    
    process_radar_files(input_directory, output_directory, zip_file_path)