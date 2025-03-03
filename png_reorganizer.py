import os
import shutil
from collections import defaultdict

def reorganize_radar_files(source_dir, target_dir, frames_per_case=29):
    """
    Function to reorganize radar PNG files - select only the lowest sweep for each time point
    
    Parameters:
    source_dir (str): Directory containing original PNG files
    target_dir (str): Directory to save reorganized files
    frames_per_case (int): Number of frames needed per case (folder)
    """
    print(f"Starting file reorganization...")
    print(f"Source directory: {source_dir}")
    print(f"Target directory: {target_dir}")
    
    os.makedirs(target_dir, exist_ok=True)
    
    # Group files by time point
    time_groups = defaultdict(list)
    
    # Collect and group all PNG files
    total_files_found = 0
    print("\nScanning for PNG files...")
    
    for root, _, files in os.walk(source_dir):
        png_files = [f for f in files if f.endswith('.png')]
        print(f"Found {len(png_files)} PNG files in this directory")
        
        for file in png_files:
            total_files_found += 1
            # Parse filename (e.g.: RDR_SSP_FQC_202501081335_sweep_1.png)
            parts = file.split('_')
            if len(parts) >= 6:
                try:
                    time_point = parts[3]  # Time information (e.g., 202501081335)
                    sweep_num = int(parts[5].split('.')[0])  # Sweep number
                    full_path = os.path.join(root, file)
                    time_groups[time_point].append((sweep_num, full_path))
                    print(f"Processed: {file} (time_point: {time_point}, sweep: {sweep_num})")
                except (ValueError, IndexError) as e:
                    print(f"Error processing file {file}: {str(e)}")
            else:
                print(f"Skipping file with unexpected format: {file}")
    
    print(f"\nTotal PNG files found: {total_files_found}")
    print(f"Unique time points found: {len(time_groups)}")
    
    # Select only the lowest sweep for each time point
    lowest_sweep_files = []
    print("\nSelecting lowest sweeps for each time point...")
    
    for time_point in sorted(time_groups.keys()):
        files = time_groups[time_point]
        if files:
            # Sort by sweep number and select the lowest
            files.sort(key=lambda x: x[0])
            lowest_sweep_files.append((time_point, files[0][1]))
            print(f"Time point {time_point}: Selected sweep {files[0][0]}")
    
    print(f"\nTotal lowest sweep files selected: {len(lowest_sweep_files)}")
    
    # Group selected files into cases with 29 frames each
    total_cases = len(lowest_sweep_files) // frames_per_case
    print(f"\nTotal number of complete cases that can be created: {total_cases}")
    
    if total_cases == 0:
        print("\nNot enough files to create complete cases!")
        print(f"Need {frames_per_case} files per case, but only found {len(lowest_sweep_files)} files")
        return
    
    # Process each case
    for case_idx in range(total_cases):
        case_id = str(case_idx).zfill(5)
        case_dir = os.path.join(target_dir, case_id)
        os.makedirs(case_dir, exist_ok=True)
        
        print(f"\nProcessing case {case_id}...")
        
        # Copy the 29 files for this case
        for frame_idx in range(frames_per_case):
            file_idx = case_idx * frames_per_case + frame_idx
            if file_idx < len(lowest_sweep_files):
                _, source_file = lowest_sweep_files[file_idx]
                new_filename = f"{case_id}-{str(frame_idx).zfill(2)}.png"
                target_file = os.path.join(case_dir, new_filename)
                
                # Copy file
                shutil.copy2(source_file, target_file)
                print(f"Copied: {new_filename}")
            else:
                print(f"Warning: Not enough source files for case {case_id}, frame {frame_idx}")
                break

if __name__ == "__main__":
    # Usage example
    source_directory = "D:/GLP/Korea_Climate_Data/KoreanPngDataset"  # Directory containing original PNG files
    target_directory = "D:/GLP/Korea_Climate_Data/ReorganizedDataset"  # Directory to save reorganized files
    
    reorganize_radar_files(source_directory, target_directory)
    print("\nFile reorganization complete!")