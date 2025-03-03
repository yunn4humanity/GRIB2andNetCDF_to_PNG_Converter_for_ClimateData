import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

def analyze_netcdf_radar(file_path):
   # NetCDF 파일 읽기
   ds = xr.open_dataset(file_path)
   
   # 1. 시간 정보 분석
   print("\n=== 1. 시간 정보 분석 ===")
   print(f"시작 시간: {ds.time_coverage_start.values}")
   print(f"종료 시간: {ds.time_coverage_end.values}")
   print("\n시간 범위:")
   print(f"첫 시간: {ds.time.values[0]}")
   print(f"마지막 시간: {ds.time.values[-1]}")
   
   # 2. 주요 레이더 변수 분석
   radar_vars = ['DBZH', 'DBZV', 'UH', 'UV', 'VELH', 'VELV', 'ZDR', 'KDP', 'RHOHV']
   
   print("\n=== 2. 주요 레이더 변수 분석 ===")
   for var_name in radar_vars:
       if var_name in ds:
           data = ds[var_name].values
           print(f"\n{var_name} 통계:")
           print(f"형태: {data.shape}")
           print(f"결측치 개수: {np.sum(np.isnan(data))}")
           print(f"결측치 비율: {(np.sum(np.isnan(data)) / data.size) * 100:.2f}%")
           valid_data = data[~np.isnan(data)]
           if len(valid_data) > 0:
               print(f"유효 데이터 범위: {np.min(valid_data):.2f} ~ {np.max(valid_data):.2f}")
               print(f"평균값: {np.mean(valid_data):.2f}")
               print(f"중앙값: {np.median(valid_data):.2f}")
   
   # 3. Sweep별 다중 변수 분석
   print("\n=== 3. Sweep별 다중 변수 분석 ===")
   
   # sweep 정보 출력
   print("\nSweep 정보:")
   print(f"고도각: {ds.fixed_angle.values}")
   print(f"Sweep 모드: {ds.sweep_mode.values}")
   
   for sweep_idx in range(len(ds.sweep_start_ray_index)):
       print(f"\nSweep {sweep_idx} 분석:")
       print(f"고도각: {ds.fixed_angle.values[sweep_idx]}도")
       
       start_idx = ds.sweep_start_ray_index[sweep_idx].values
       end_idx = ds.sweep_end_ray_index[sweep_idx].values
       
       # 각 변수별 분석
       for var_name in radar_vars:
           if var_name in ds:
               start_gate_idx = start_idx * len(ds['range'])
               end_gate_idx = (end_idx + 1) * len(ds['range'])
               sweep_data = ds[var_name].values[start_gate_idx:end_gate_idx].reshape(-1, len(ds['range']))
               
               valid_data = sweep_data[~np.isnan(sweep_data)]
               if len(valid_data) > 0:
                   print(f"\n{var_name}:")
                   print(f"유효 데이터 개수: {len(valid_data)}")
                   print(f"데이터 범위: {np.min(valid_data):.2f} ~ {np.max(valid_data):.2f}")
                   
                   # 데이터 분포 시각화
                   plt.figure(figsize=(12, 5))
                   
                   # subplot 1: 히스토그램
                   plt.subplot(121)
                   plt.hist(valid_data, bins=50, density=True)
                   plt.title(f'{var_name} Distribution - Sweep {sweep_idx}')
                   plt.xlabel('Value')
                   plt.ylabel('Density')
                   
                   # subplot 2: 2D plot
                   plt.subplot(122)
                   plt.imshow(sweep_data, cmap='rainbow', origin='lower')
                   plt.colorbar(label=f'{var_name} [{ds[var_name].units}]')
                   plt.title(f'{var_name} Data - Sweep {sweep_idx}')
                   
                   plt.tight_layout()
                   plt.savefig(f'{var_name}_sweep_{sweep_idx}_analysis.png')
                   plt.close()

   ds.close()

# 함수 실행
analyze_netcdf_radar('korea_data.nc')