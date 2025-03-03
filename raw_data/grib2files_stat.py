import os
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import tqdm.auto as tqdm  # 이 부분을 수정했습니다

def analyze_missing_values():
    # 현재 디렉토리의 모든 .grib2 파일 찾기 (grib2 파일을 저장한 디렉토리와 동일한 디렉토리에 파일을 위치할 것)
    grib_files = [f for f in os.listdir() if f.endswith('.grib2')]
    
    if not grib_files:
        print("현재 폴더에 .grib2 파일이 없습니다.")
        return
    
    print(f"총 {len(grib_files)}개의 .grib2 파일을 분석합니다.")
    
    # 결측치 비율을 저장할 딕셔너리
    missing_ratios = {}
    
    # 각 파일 분석
    progress_bar = tqdm.tqdm(grib_files, desc="파일 분석 중")  
    for grib_file in progress_bar:
        try:
            # grib 파일 읽기
            ds = xr.open_dataset(grib_file, engine='cfgrib')
            
            # 첫 번째 변수 선택 (보통 precipitation rate)
            var_name = list(ds.data_vars)[0]
            data = ds[var_name].values
            
            # 결측치 비율 계산 (nan 값의 비율)
            missing_ratio = (np.isnan(data).sum() / data.size) * 100
            missing_ratios[grib_file] = missing_ratio
            
            # 데이터셋 닫기
            ds.close()
            
        except Exception as e:
            print(f'\n파일 분석 중 오류 발생 {grib_file}: {str(e)}')
            continue
    
    # 결과 출력 및 시각화
    print("\n결측치 분석 결과:")
    print("\n상위 10개 결측치가 많은 파일:")
    sorted_files = sorted(missing_ratios.items(), key=lambda x: x[1], reverse=True)
    for file, ratio in sorted_files[:10]:
        print(f"{file}: {ratio:.2f}%")
    
    # 히스토그램 그리기
    plt.figure(figsize=(10, 6))
    plt.hist(list(missing_ratios.values()), bins=50)
    plt.title('GRIB2 파일의 결측치 분포')
    plt.xlabel('결측치 비율 (%)')
    plt.ylabel('파일 수')
    plt.grid(True)
    plt.savefig('missing_values_distribution.png')
    plt.close()
    
    # 기본 통계 출력
    ratios = np.array(list(missing_ratios.values()))
    print(f"\n기본 통계:")
    print(f"평균 결측치 비율: {np.mean(ratios):.2f}%")
    print(f"중앙값: {np.median(ratios):.2f}%")
    print(f"최소값: {np.min(ratios):.2f}%")
    print(f"최대값: {np.max(ratios):.2f}%")
    
    return missing_ratios

if __name__ == "__main__":
    # 필요한 패키지 설치 안내
    try:
        import xarray as xr
        import cfgrib
    except ImportError:
        print("필요한 패키지를 설치해주세요:")
        print("pip install xarray cfgrib tqdm matplotlib numpy")
        exit(1)
    
    missing_ratios = analyze_missing_values()