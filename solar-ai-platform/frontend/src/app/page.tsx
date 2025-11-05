'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Sun, MapPin, TrendingUp, Leaf, ArrowRight, Check } from 'lucide-react';

export default function HomePage() {
  const [address, setAddress] = useState('');
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!address.trim()) {
      alert('주소를 입력해주세요.');
      return;
    }

    setLoading(true);

    try {
      const response = await fetch('http://localhost:8000/api/v1/analysis', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          address: address,
          building_type: 'house'
        }),
      });

      if (!response.ok) {
        throw new Error('분석 요청 실패');
      }

      const data = await response.json();
      router.push(`/analysis/${data.request_id}`);
    } catch (error) {
      console.error('Error:', error);
      alert('분석 요청에 실패했습니다. 다시 시도해주세요.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-green-50">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Sun className="w-8 h-8 text-yellow-500" />
            <span className="text-2xl font-bold bg-gradient-to-r from-yellow-500 to-orange-500 bg-clip-text text-transparent">
              SolarScan
            </span>
          </div>
          <nav className="hidden md:flex gap-6">
            <a href="#features" className="text-gray-600 hover:text-gray-900">기능</a>
            <a href="#how-it-works" className="text-gray-600 hover:text-gray-900">사용방법</a>
            <a href="#pricing" className="text-gray-600 hover:text-gray-900">가격</a>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20 text-center">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-5xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-blue-600 via-green-600 to-yellow-600 bg-clip-text text-transparent">
            AI가 분석하는
            <br />
            태양광 설치 최적화
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            경기도 기후 데이터 기반으로 당신의 집에 태양광을 설치하면
            <br />
            얼마나 절약할 수 있는지 30초 만에 확인하세요
          </p>

          {/* Search Form */}
          <form onSubmit={handleSubmit} className="max-w-2xl mx-auto mb-12">
            <div className="flex gap-3 p-2 bg-white rounded-2xl shadow-xl">
              <div className="flex-1 flex items-center gap-3 px-4">
                <MapPin className="w-5 h-5 text-gray-400" />
                <input
                  type="text"
                  value={address}
                  onChange={(e) => setAddress(e.target.value)}
                  placeholder="주소를 입력하세요 (예: 경기도 수원시 영통구 광교로 156)"
                  className="flex-1 outline-none text-lg"
                  disabled={loading}
                />
              </div>
              <button
                type="submit"
                disabled={loading}
                className="px-8 py-4 bg-gradient-to-r from-yellow-500 to-orange-500 text-white rounded-xl font-semibold hover:shadow-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
              >
                {loading ? (
                  <>
                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                    분석 중...
                  </>
                ) : (
                  <>
                    분석 시작
                    <ArrowRight className="w-5 h-5" />
                  </>
                )}
              </button>
            </div>
          </form>

          {/* Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-3xl mx-auto">
            <div className="bg-white/80 backdrop-blur-sm p-6 rounded-xl shadow-md">
              <div className="text-3xl font-bold text-blue-600 mb-2">10,000+</div>
              <div className="text-gray-600">분석 완료</div>
            </div>
            <div className="bg-white/80 backdrop-blur-sm p-6 rounded-xl shadow-md">
              <div className="text-3xl font-bold text-green-600 mb-2">95%+</div>
              <div className="text-gray-600">예측 정확도</div>
            </div>
            <div className="bg-white/80 backdrop-blur-sm p-6 rounded-xl shadow-md">
              <div className="text-3xl font-bold text-yellow-600 mb-2">30초</div>
              <div className="text-gray-600">분석 소요 시간</div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="bg-white py-20">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-12">
            왜 SolarScan인가요?
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            <FeatureCard
              icon={<Sun className="w-12 h-12 text-yellow-500" />}
              title="정확한 발전량 예측"
              description="AI 모델이 기후 데이터를 분석하여 월별 발전량을 정확하게 예측합니다"
            />
            <FeatureCard
              icon={<TrendingUp className="w-12 h-12 text-green-500" />}
              title="투자 수익 분석"
              description="설치 비용, 보조금, 절감액을 계산하여 투자 회수 기간을 알려드립니다"
            />
            <FeatureCard
              icon={<MapPin className="w-12 h-12 text-blue-500" />}
              title="지붕 자동 분석"
              description="위성 이미지로 지붕 면적, 방향, 경사각을 자동으로 분석합니다"
            />
            <FeatureCard
              icon={<Leaf className="w-12 h-12 text-emerald-500" />}
              title="환경 기여도"
              description="CO2 감축량과 나무 심기 효과를 환산하여 보여드립니다"
            />
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section id="how-it-works" className="py-20">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-12">
            어떻게 작동하나요?
          </h2>
          <div className="max-w-4xl mx-auto">
            <div className="space-y-8">
              <Step
                number={1}
                title="주소 입력"
                description="분석하고 싶은 주택의 주소를 입력하세요"
              />
              <Step
                number={2}
                title="AI 분석"
                description="경기도 기후 데이터와 위성 이미지를 AI가 자동으로 분석합니다"
              />
              <Step
                number={3}
                title="결과 확인"
                description="30초 후 발전량, 절감액, 투자 수익률 등 상세 분석 결과를 확인하세요"
              />
              <Step
                number={4}
                title="설치 업체 연결"
                description="원하시면 검증된 설치 업체와 바로 연결해드립니다"
              />
            </div>
          </div>
        </div>
      </section>

      {/* Pricing */}
      <section id="pricing" className="bg-white py-20">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-12">
            요금 안내
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            <PricingCard
              name="무료"
              price="₩0"
              features={[
                "기본 분석 결과",
                "발전량 예측",
                "절감액 계산",
                "1회 분석"
              ]}
              buttonText="무료로 시작"
              highlighted={false}
            />
            <PricingCard
              name="프리미엄"
              price="₩29,000"
              features={[
                "상세 PDF 리포트",
                "20년 시뮬레이션",
                "최적 설치 용량 추천",
                "업체별 견적 비교",
                "이메일 지원"
              ]}
              buttonText="프리미엄 구매"
              highlighted={true}
            />
            <PricingCard
              name="기업"
              price="₩99,000/월"
              features={[
                "무제한 분석",
                "API 연동",
                "고객용 브랜딩",
                "우선 지원",
                "전담 매니저"
              ]}
              buttonText="문의하기"
              highlighted={false}
            />
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center gap-2 mb-4">
                <Sun className="w-6 h-6 text-yellow-500" />
                <span className="text-xl font-bold">SolarScan</span>
              </div>
              <p className="text-gray-400">
                AI 기반 태양광 설치 최적화 플랫폼
              </p>
            </div>
            <div>
              <h3 className="font-semibold mb-4">서비스</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white">분석 시작</a></li>
                <li><a href="#" className="hover:text-white">비교 분석</a></li>
                <li><a href="#" className="hover:text-white">히트맵</a></li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold mb-4">회사</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white">소개</a></li>
                <li><a href="#" className="hover:text-white">팀</a></li>
                <li><a href="#" className="hover:text-white">채용</a></li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold mb-4">문의</h3>
              <ul className="space-y-2 text-gray-400">
                <li>이메일: contact@solarscan.kr</li>
                <li>전화: 031-XXX-XXXX</li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2025 SolarScan. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

function FeatureCard({ icon, title, description }: { icon: React.ReactNode; title: string; description: string }) {
  return (
    <div className="p-6 rounded-xl bg-gradient-to-br from-white to-gray-50 shadow-md hover:shadow-xl transition-shadow">
      <div className="mb-4">{icon}</div>
      <h3 className="text-xl font-semibold mb-2">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </div>
  );
}

function Step({ number, title, description }: { number: number; title: string; description: string }) {
  return (
    <div className="flex gap-6 items-start">
      <div className="flex-shrink-0 w-12 h-12 rounded-full bg-gradient-to-r from-yellow-500 to-orange-500 flex items-center justify-center text-white font-bold text-xl">
        {number}
      </div>
      <div className="flex-1">
        <h3 className="text-2xl font-semibold mb-2">{title}</h3>
        <p className="text-gray-600">{description}</p>
      </div>
    </div>
  );
}

function PricingCard({ 
  name, 
  price, 
  features, 
  buttonText, 
  highlighted 
}: { 
  name: string; 
  price: string; 
  features: string[]; 
  buttonText: string; 
  highlighted: boolean;
}) {
  return (
    <div className={`p-8 rounded-2xl ${highlighted ? 'bg-gradient-to-br from-yellow-500 to-orange-500 text-white shadow-2xl scale-105' : 'bg-white shadow-md'}`}>
      <h3 className="text-2xl font-bold mb-2">{name}</h3>
      <div className="text-4xl font-bold mb-6">{price}</div>
      <ul className="space-y-3 mb-8">
        {features.map((feature, index) => (
          <li key={index} className="flex items-center gap-2">
            <Check className="w-5 h-5 flex-shrink-0" />
            <span>{feature}</span>
          </li>
        ))}
      </ul>
      <button className={`w-full py-3 rounded-xl font-semibold transition-all ${highlighted ? 'bg-white text-orange-500 hover:bg-gray-100' : 'bg-gradient-to-r from-yellow-500 to-orange-500 text-white hover:shadow-lg'}`}>
        {buttonText}
      </button>
    </div>
  );
}

