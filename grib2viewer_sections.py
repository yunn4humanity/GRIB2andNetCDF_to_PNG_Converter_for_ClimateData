import pygrib
import numpy as np
from datetime import datetime

def safe_get(grb, attr, default="Not available"):
    """안전하게 속성을 가져오는 헬퍼 함수"""
    try:
        return grb[attr] if attr in grb.keys() else default
    except:
        return default

def analyze_grib2(file_path):
    try:
        # GRIB2 파일 열기
        grbs = pygrib.open(file_path)
        
        print("=== GRIB2 파일 구조 분석 ===\n")
        
        # 모든 메시지 순회
        for i, grb in enumerate(grbs, 1):
            print(f"\n메시지 #{i}")
            print("="* 50)
            
            # 1. Indicator Section & 2. Identification Section
            print("\n[식별 정보]")
            print(f"• 발표 센터: {safe_get(grb, 'centre')}")
            try:
                print(f"• 생성 시각: {datetime.fromtimestamp(grb.timeStamp)}")
            except:
                print("• 생성 시각: Not available")
            try:
                print(f"• 참조 시각: {grb.validDate}")
            except:
                print("• 참조 시각: Not available")
            
            # 4. Grid Description Section
            print("\n[격자 정보]")
            print(f"• 격자 종류: {safe_get(grb, 'gridType')}")
            print(f"• 격자점 수: {safe_get(grb, 'numberOfPoints')}")
            
            # 위도/경도 정보 안전하게 가져오기
            try:
                lat_first = safe_get(grb, 'latitudeOfFirstGridPointInDegrees')
                lat_last = safe_get(grb, 'latitudeOfLastGridPointInDegrees')
                if lat_first != "Not available" and lat_last != "Not available":
                    print(f"• 위도 범위: {lat_first:.2f}° ~ {lat_last:.2f}°")
                else:
                    print("• 위도 범위: Not available")
            except:
                print("• 위도 범위: Not available")
                
            try:
                lon_first = safe_get(grb, 'longitudeOfFirstGridPointInDegrees')
                lon_last = safe_get(grb, 'longitudeOfLastGridPointInDegrees')
                if lon_first != "Not available" and lon_last != "Not available":
                    print(f"• 경도 범위: {lon_first:.2f}° ~ {lon_last:.2f}°")
                else:
                    print("• 경도 범위: Not available")
            except:
                print("• 경도 범위: Not available")
            
            # 5. Product Definition Section
            print("\n[변수 정보]")
            print(f"• 변수명: {safe_get(grb, 'name')}")
            print(f"• 단위: {safe_get(grb, 'units')}")
            print(f"• 고도: {safe_get(grb, 'level')}")
            
            # 6. Data Representation Section
            print("\n[데이터 표현 정보]")
            print(f"• 압축 방식: {safe_get(grb, 'packingType')}")
            print(f"• 누락값: {safe_get(grb, 'missingValue')}")
            
            # 7 & 8. Bitmap & Data Section
            try:
                data = grb.values
                print("\n[데이터 통계]")
                print(f"• 데이터 형태: {data.shape}")
                print(f"• 최소값: {np.min(data):.2f}")
                print(f"• 최대값: {np.max(data):.2f}")
                print(f"• 평균값: {np.mean(data):.2f}")
                print(f"• 표준편차: {np.std(data):.2f}")
            except:
                print("\n[데이터 통계]")
                print("• 데이터 통계를 계산할 수 없습니다.")
            
            # 사용 가능한 모든 키 출력
            print("\n[사용 가능한 모든 키]")
            for key in grb.keys():
                if key not in ['values', 'latitudes', 'longitudes'] and not key.startswith('_'):
                    print(f"• {key}: {safe_get(grb, key)}")
            
            print("\n" + "="*50)
    
    except Exception as e:
        print(f"오류 발생: {str(e)}")
    
    finally:
        if 'grbs' in locals():
            grbs.close()

# 사용 예시
file_path = 'usa_data.grib2'  # 분석할 GRIB2 파일 경로
analyze_grib2(file_path)