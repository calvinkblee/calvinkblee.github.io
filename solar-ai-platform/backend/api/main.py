"""
SolarScan FastAPI Main Application
경기도 기후플랫폼 기반 AI 태양광 설치 분석 API
"""

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
import uuid
from datetime import datetime
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI 앱 생성
app = FastAPI(
    title="SolarScan API",
    description="AI 기반 태양광 설치 최적화 플랫폼",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://solarscan.kr",
        "https://www.solarscan.kr"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== Request/Response Models ====================

class AnalysisRequest(BaseModel):
    """분석 요청 모델"""
    address: str = Field(
        ...,
        description="분석할 주소",
        example="경기도 수원시 영통구 광교로 156"
    )
    building_type: str = Field(
        default="house",
        description="건물 유형 (house: 단독주택, apartment: 아파트)",
        example="house"
    )
    email: Optional[EmailStr] = Field(
        None,
        description="결과 수신 이메일 (선택)",
        example="user@example.com"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "address": "경기도 수원시 영통구 광교로 156",
                "building_type": "house",
                "email": "user@example.com"
            }
        }


class AnalysisResponse(BaseModel):
    """분석 요청 응답 모델"""
    request_id: str
    status: str
    message: str
    estimated_time: int = Field(description="예상 소요 시간 (초)")


class LocationInfo(BaseModel):
    """위치 정보"""
    address: str
    latitude: float
    longitude: float
    region: str  # 시/군/구


class RoofAnalysis(BaseModel):
    """지붕 분석 결과"""
    roof_area: float = Field(description="지붕 면적 (m²)")
    roof_direction: str = Field(description="지붕 방향 (N, NE, E, SE, S, SW, W, NW)")
    roof_angle: float = Field(description="지붕 경사각 (도)")
    usable_area: float = Field(description="사용 가능 면적 (m²)")
    obstacles: List[Dict[str, Any]] = Field(description="장애물 목록")
    optimal_panel_layout: Dict[str, Any] = Field(description="최적 패널 배치")


class SolarPrediction(BaseModel):
    """태양광 발전량 예측"""
    recommended_capacity: float = Field(description="권장 설치 용량 (kW)")
    panel_count: int = Field(description="패널 수량")
    annual_generation: float = Field(description="연간 예상 발전량 (kWh)")
    monthly_generation: Dict[str, float] = Field(description="월별 발전량")
    daily_average: float = Field(description="일평균 발전량 (kWh)")
    confidence_score: float = Field(description="예측 신뢰도 (0-1)")


class EconomicAnalysis(BaseModel):
    """경제성 분석"""
    installation_cost: int = Field(description="설치 비용 (원)")
    subsidy_amount: int = Field(description="보조금 (원)")
    net_cost: int = Field(description="실제 부담 비용 (원)")
    annual_savings: int = Field(description="연간 절감액 (원)")
    monthly_savings: int = Field(description="월간 절감액 (원)")
    payback_period: float = Field(description="투자 회수 기간 (년)")
    roi_20years: int = Field(description="20년 누적 수익 (원)")
    electricity_rate: int = Field(description="전기요금 단가 (원/kWh)")


class EnvironmentalImpact(BaseModel):
    """환경 기여도"""
    co2_reduction: float = Field(description="CO2 감축량 (톤/년)")
    tree_equivalent: int = Field(description="나무 심기 환산 (그루)")
    oil_savings: float = Field(description="석유 절감량 (리터/년)")


class AnalysisResult(BaseModel):
    """전체 분석 결과"""
    request_id: str
    status: str
    location: LocationInfo
    roof_analysis: RoofAnalysis
    solar_prediction: SolarPrediction
    economic_analysis: EconomicAnalysis
    environmental_impact: EnvironmentalImpact
    created_at: str
    completed_at: str


class CompareRequest(BaseModel):
    """비교 분석 요청"""
    addresses: List[str] = Field(
        ...,
        min_length=2,
        max_length=5,
        description="비교할 주소 목록 (2-5개)"
    )


# ==================== Helper Functions ====================

async def geocode_address(address: str) -> Optional[Dict]:
    """
    주소를 좌표로 변환 (Kakao API 사용)
    실제 구현에서는 Kakao Local API 호출
    """
    # TODO: Kakao API 연동
    # 임시 더미 데이터
    return {
        "address": address,
        "latitude": 37.2858,
        "longitude": 127.0444,
        "region": "경기도 수원시 영통구"
    }


async def process_analysis(
    request_id: str,
    address: str,
    location: Dict,
    building_type: str,
    email: Optional[str] = None
):
    """
    비동기 분석 처리 (Celery Task로 실행)
    """
    try:
        logger.info(f"Starting analysis for request_id: {request_id}")
        
        # 1. 경기도 기후 데이터 수집
        climate_data = await fetch_climate_data(
            location['latitude'],
            location['longitude']
        )
        
        # 2. 위성 이미지 분석 (지붕)
        roof_result = await analyze_roof_from_satellite(
            location['latitude'],
            location['longitude']
        )
        
        # 3. AI 발전량 예측
        solar_prediction = await predict_solar_generation(
            climate_data,
            roof_result
        )
        
        # 4. 경제성 분석
        economic_result = await calculate_economics(
            solar_prediction,
            location['region']
        )
        
        # 5. 환경 기여도 계산
        environmental_result = calculate_environmental_impact(
            solar_prediction['annual_generation']
        )
        
        # 6. 결과 저장
        result = {
            'request_id': request_id,
            'status': 'completed',
            'location': location,
            'roof_analysis': roof_result,
            'solar_prediction': solar_prediction,
            'economic_analysis': economic_result,
            'environmental_impact': environmental_result,
            'created_at': datetime.utcnow().isoformat(),
            'completed_at': datetime.utcnow().isoformat()
        }
        
        # TODO: DB에 저장
        # await save_result_to_db(result)
        
        # 이메일 전송 (선택)
        if email:
            await send_result_email(email, result)
        
        logger.info(f"Analysis completed for request_id: {request_id}")
        
    except Exception as e:
        logger.error(f"Analysis failed for request_id {request_id}: {str(e)}")
        # TODO: 실패 상태 DB 업데이트


async def fetch_climate_data(lat: float, lon: float) -> Dict:
    """경기도 기후플랫폼에서 데이터 수집"""
    # TODO: 실제 API 연동
    return {
        'solar_radiation_monthly': [2.5, 3.0, 3.8, 4.5, 5.2, 5.5, 5.3, 5.0, 4.2, 3.5, 2.8, 2.3],
        'temperature_monthly': [-2, 1, 7, 13, 18, 23, 26, 27, 22, 15, 8, 1],
        'annual_avg_solar_radiation': 4.0,
        'sunshine_hours': 2500
    }


async def analyze_roof_from_satellite(lat: float, lon: float) -> Dict:
    """위성 이미지 기반 지붕 분석"""
    # TODO: Computer Vision 모델 연동
    return {
        'roof_area': 150.0,
        'roof_direction': 'S',
        'roof_angle': 25.0,
        'usable_area': 135.0,
        'obstacles': [
            {'type': 'chimney', 'area': 2.5},
            {'type': 'skylight', 'area': 5.0}
        ],
        'optimal_panel_layout': {
            'rows': 6,
            'columns': 10,
            'panel_count': 60,
            'total_capacity': 18.0
        }
    }


async def predict_solar_generation(climate_data: Dict, roof_data: Dict) -> Dict:
    """AI 모델을 사용한 발전량 예측"""
    # TODO: XGBoost 모델 연동
    
    capacity = roof_data['optimal_panel_layout']['total_capacity']
    monthly_gen = []
    
    for month_radiation in climate_data['solar_radiation_monthly']:
        # 간단한 계산식 (실제로는 AI 모델 사용)
        daily_gen = capacity * month_radiation * 0.85  # 효율 85%
        days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        month_idx = len(monthly_gen)
        monthly_total = daily_gen * days_in_month[month_idx]
        monthly_gen.append(round(monthly_total, 2))
    
    annual_gen = sum(monthly_gen)
    
    return {
        'recommended_capacity': capacity,
        'panel_count': roof_data['optimal_panel_layout']['panel_count'],
        'annual_generation': round(annual_gen, 2),
        'monthly_generation': {str(i+1): gen for i, gen in enumerate(monthly_gen)},
        'daily_average': round(annual_gen / 365, 2),
        'confidence_score': 0.92
    }


async def calculate_economics(solar_prediction: Dict, region: str) -> Dict:
    """경제성 분석"""
    capacity = solar_prediction['recommended_capacity']
    annual_gen = solar_prediction['annual_generation']
    
    # 설치 비용 (kW당 약 500만원)
    installation_cost = int(capacity * 5_000_000)
    
    # 보조금 (지역별 차등, 여기서는 평균)
    subsidy_amount = int(capacity * 1_000_000)
    
    # 실제 부담 비용
    net_cost = installation_cost - subsidy_amount
    
    # 전기요금 절감 (kWh당 150원)
    electricity_rate = 150
    annual_savings = int(annual_gen * electricity_rate)
    monthly_savings = int(annual_savings / 12)
    
    # 투자 회수 기간
    payback_period = round(net_cost / annual_savings, 1) if annual_savings > 0 else 0
    
    # 20년 누적 수익
    roi_20years = (annual_savings * 20) - net_cost
    
    return {
        'installation_cost': installation_cost,
        'subsidy_amount': subsidy_amount,
        'net_cost': net_cost,
        'annual_savings': annual_savings,
        'monthly_savings': monthly_savings,
        'payback_period': payback_period,
        'roi_20years': roi_20years,
        'electricity_rate': electricity_rate
    }


def calculate_environmental_impact(annual_generation: float) -> Dict:
    """환경 기여도 계산"""
    # CO2 감축: 1kWh = 0.424kg CO2
    co2_reduction = round(annual_generation * 0.424 / 1000, 2)  # 톤
    
    # 나무 심기 환산: 나무 1그루 = 연간 6.6kg CO2 흡수
    tree_equivalent = int(co2_reduction * 1000 / 6.6)
    
    # 석유 절감: 1kWh = 0.22리터 석유
    oil_savings = round(annual_generation * 0.22, 2)
    
    return {
        'co2_reduction': co2_reduction,
        'tree_equivalent': tree_equivalent,
        'oil_savings': oil_savings
    }


async def send_result_email(email: str, result: Dict):
    """결과 이메일 전송"""
    # TODO: SMTP 연동
    logger.info(f"Sending result email to {email}")


async def get_result_from_db(request_id: str) -> Optional[Dict]:
    """DB에서 결과 조회"""
    # TODO: DB 연동
    # 임시 더미 데이터
    return None


# ==================== API Endpoints ====================

@app.get("/")
async def root():
    """API 루트"""
    return {
        "service": "SolarScan API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """헬스 체크"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/api/v1/analysis", response_model=AnalysisResponse)
async def create_analysis(
    request: AnalysisRequest,
    background_tasks: BackgroundTasks
):
    """
    태양광 설치 분석 요청
    
    - **address**: 분석할 주소 (필수)
    - **building_type**: 건물 유형 (house, apartment)
    - **email**: 결과 수신 이메일 (선택)
    
    Returns:
        - request_id: 분석 요청 ID
        - status: 처리 상태
        - message: 안내 메시지
        - estimated_time: 예상 소요 시간 (초)
    """
    try:
        # 주소 검증 및 좌표 변환
        geocode_result = await geocode_address(request.address)
        
        if not geocode_result:
            raise HTTPException(
                status_code=400,
                detail="유효하지 않은 주소입니다. 주소를 다시 확인해주세요."
            )
        
        # 경기도 지역 확인
        if "경기도" not in geocode_result.get("region", ""):
            raise HTTPException(
                status_code=400,
                detail="현재 경기도 지역만 지원합니다."
            )
        
        # 요청 ID 생성
        request_id = str(uuid.uuid4())
        
        # 비동기 분석 작업 시작
        background_tasks.add_task(
            process_analysis,
            request_id=request_id,
            address=request.address,
            location=geocode_result,
            building_type=request.building_type,
            email=request.email
        )
        
        logger.info(f"Analysis request created: {request_id} for {request.address}")
        
        return AnalysisResponse(
            request_id=request_id,
            status="processing",
            message="분석이 시작되었습니다. 약 30초 후 결과를 확인할 수 있습니다.",
            estimated_time=30
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating analysis: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="분석 요청 처리 중 오류가 발생했습니다."
        )


@app.get("/api/v1/analysis/{request_id}")
async def get_analysis_result(request_id: str):
    """
    분석 결과 조회
    
    - **request_id**: 분석 요청 ID
    
    Returns:
        - 분석 완료 시: 전체 결과
        - 분석 중: status = processing
        - 실패: status = failed
    """
    try:
        result = await get_result_from_db(request_id)
        
        if not result:
            # 임시 더미 데이터 반환 (개발용)
            return {
                "request_id": request_id,
                "status": "processing",
                "message": "분석이 진행 중입니다.",
                "progress": 75
            }
        
        return result
        
    except Exception as e:
        logger.error(f"Error fetching result: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="결과 조회 중 오류가 발생했습니다."
        )


@app.post("/api/v1/compare")
async def compare_locations(request: CompareRequest):
    """
    여러 주소 비교 분석
    
    - **addresses**: 비교할 주소 목록 (2-5개)
    
    Returns:
        - 각 주소별 분석 결과 및 비교 차트 데이터
    """
    try:
        if len(request.addresses) < 2 or len(request.addresses) > 5:
            raise HTTPException(
                status_code=400,
                detail="2개에서 5개 사이의 주소를 입력해주세요."
            )
        
        results = []
        for address in request.addresses:
            geocode_result = await geocode_address(address)
            if geocode_result:
                # 간단한 분석 (빠른 비교용)
                climate_data = await fetch_climate_data(
                    geocode_result['latitude'],
                    geocode_result['longitude']
                )
                
                results.append({
                    'address': address,
                    'location': geocode_result,
                    'avg_solar_radiation': climate_data['annual_avg_solar_radiation'],
                    'estimated_annual_generation': 3500,  # 임시값
                    'estimated_annual_savings': 525000  # 임시값
                })
        
        # 비교 차트 데이터 생성
        comparison = {
            'results': results,
            'best_location': max(results, key=lambda x: x['avg_solar_radiation']),
            'comparison_metrics': {
                'solar_radiation': [r['avg_solar_radiation'] for r in results],
                'annual_generation': [r['estimated_annual_generation'] for r in results],
                'annual_savings': [r['estimated_annual_savings'] for r in results]
            }
        }
        
        return comparison
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in comparison: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="비교 분석 중 오류가 발생했습니다."
        )


@app.get("/api/v1/heatmap")
async def get_solar_heatmap(
    region: str = "gyeonggi",
    metric: str = "solar_radiation"
):
    """
    경기도 일사량 히트맵 데이터
    
    - **region**: 지역 (gyeonggi)
    - **metric**: 지표 (solar_radiation, cost_savings, roi)
    
    Returns:
        - GeoJSON 형식의 히트맵 데이터
    """
    try:
        # TODO: 실제 히트맵 데이터 생성
        heatmap_data = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [127.0444, 37.2858]
                    },
                    "properties": {
                        "value": 4.5,
                        "city": "수원시"
                    }
                }
                # ... 더 많은 데이터 포인트
            ]
        }
        
        return heatmap_data
        
    except Exception as e:
        logger.error(f"Error generating heatmap: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="히트맵 데이터 생성 중 오류가 발생했습니다."
        )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """전역 예외 처리"""
    logger.error(f"Global exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요.",
            "error_id": str(uuid.uuid4())
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

