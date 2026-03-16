# MONO — Dress Shop Digital Lookbook

## 프로젝트 개요

드레스샵 매장용 디지털 룩북. 고객이 매장 방문 시 태블릿/웹에서 드레스를 탐색하고, 원하는 드레스를 선택하면 해당 드레스의 다양한 모습을 고급스러운 풀스크린 슬라이드쇼로 보여주는 앱.

- **용도**: 매장 내 고객 응대용 (홈페이지 아님)
- **디자인 톤**: 모노톤(흑백), 미니멀, 고급스러운 느낌
- **타겟 디바이스**: 태블릿 + 웹 브라우저
- **기술 스택**: HTML, Tailwind CSS v4, Vanilla JS

---

## 폴더 구조

```
lookbook/
├── index.html              # 메인 페이지 (드레스 그리드 + 슬라이드쇼)
├── package.json            # npm 스크립트 (build, dev)
├── package-lock.json
├── .env                    # API 키 (Google Gemini - 이미지 생성용)
├── PROJECT.md              # 이 파일 (프로젝트 안내)
├── SKILL.md                # 개발 스킬 가이드 (Claude Code용)
├── src/
│   └── input.css           # Tailwind 입력 CSS (커스텀 테마 정의)
├── dist/
│   └── output.css          # Tailwind 빌드된 프로덕션 CSS
├── images/                 # (생성 예정) 드레스 이미지 폴더
│   ├── dress-01/
│   │   ├── thumb.png
│   │   ├── view-1.png
│   │   ├── view-2.png
│   │   └── view-3.png
│   └── dress-02/
│       └── ...
└── node_modules/
```

---

## 실행 방법

### CSS 빌드
```bash
# 프로덕션 빌드 (minified)
npm run build

# 개발 모드 (watch - 변경 시 자동 빌드)
npm run dev
```

### 로컬 서버 (선택)
```bash
# 간단한 로컬 서버
npx serve .
# 또는
python3 -m http.server 8080
```

---

## 주요 기능

### 1. 드레스 그리드 (메인 화면)
- 2~4컬럼 반응형 그리드 (모바일 2열 → 태블릿 3열 → 데스크탑 4열)
- 카테고리 필터: All / Wedding / Evening / Cocktail / Classic
- 호버 시 드레스명, 스타일, 이미지 수 표시
- 필터 전환 시 페이드 애니메이션

### 2. 풀스크린 슬라이드쇼 (드레스 선택 시)
- 드레스 클릭 → 해당 드레스의 10장 뷰 풀스크린으로 전환
- 좌우 화살표 버튼 / 키보드 Arrow / 터치 스와이프 탐색
- 하단 썸네일 스트립으로 빠른 이동
- 프로그레스 바 + 슬라이드 카운터 (01 / 04)
- Auto 버튼으로 자동 슬라이드 (3.5초 간격)
- ESC 또는 X 버튼으로 닫기

### 3. 반응형 레이아웃
- 태블릿 (768px+): 3컬럼 그리드, 터치 스와이프
- 데스크탑 (1024px+): 4컬럼 그리드, 키보드 네비게이션

---

## 드레스 데이터 구조

`index.html` 내 `dresses` 배열에 정의됨:

```javascript
{
    id: 1,
    name: "Ethereal Veil Gown",      // 드레스 이름
    style: "Wedding",                 // 표시용 스타일명
    category: "wedding",              // 필터 카테고리 (wedding/evening/cocktail/classic)
    thumbnail: "images/dress-01/thumb.png",  // 그리드 썸네일
    images: [                          // 슬라이드쇼 이미지들 (다양한 앵글)
        "images/dress-01/view-1.png",
        "images/dress-01/view-2.png",
        "images/dress-01/view-3.png",
        "images/dress-01/view-4.png"
    ]
}
```

---

## 후속 개발 TODO

### 우선순위 높음
- [ ] Google Imagen API로 드레스 이미지 생성 (generate_images.py 스크립트 필요)
- [ ] 생성된 이미지를 `images/` 폴더에 저장 후 dresses 배열의 URL을 로컬 경로로 교체
- [ ] 실제 매장 드레스 사진으로 교체 (촬영 후)

### 기능 추가
- [ ] 드레스 상세 정보 패널 (가격, 소재, 사이즈 등)
- [ ] 즐겨찾기/픽 기능 (고객이 마음에 드는 드레스 저장)
- [ ] 드레스 비교 기능 (2~3벌 나란히 비교)
- [ ] 검색 기능
- [ ] 관리자 페이지 (드레스 추가/삭제/수정)

### 디자인 개선
- [ ] 로딩 스켈레톤 UI
- [ ] 이미지 줌 인/아웃 기능 (핀치 줌)
- [ ] 페이지 전환 애니메이션 강화
- [ ] 다크/라이트 모드 토글

---

## 이미지 생성 API 정보

### Google Gemini (Imagen 3)
- 모델: `imagen-3.0-generate-002`
- API 키: `.env` 파일의 `GOOGLE_API_KEY`
- 비율: `3:4` (드레스에 적합)
- SDK: `pip install google-genai`

### 프롬프트 가이드 (드레스 이미지)
```
기본 프롬프트 구조:
"A luxurious [스타일] dress, [색상/소재 설명], studio photography,
soft dramatic lighting, black background, high fashion editorial,
full body mannequin display, monochrome, 8K quality"

앵글별 프롬프트:
- 전면: "front view, full length"
- 측면: "side profile view, showing silhouette"
- 후면: "back view, showing details"
- 클로즈업: "close-up detail shot, fabric texture, embroidery"
```

---

## 현재 이미지 상태

현재 모든 이미지는 **Unsplash 외부 URL**로 연결되어 있음 (placeholder).
실제 사용 시 로컬 이미지로 교체 필요.
