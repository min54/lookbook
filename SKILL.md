# MONO Dress Lookbook — 개발 스킬 가이드

이 문서는 Claude Code에서 후속 개발할 때 참고하는 스킬 가이드입니다.

---

## 프로젝트 컨텍스트

- **목적**: 드레스샵 매장 내 고객용 디지털 룩북
- **사용 시나리오**: 고객이 드레스 그리드에서 탐색 → 드레스 선택 → 풀스크린 슬라이드쇼로 다양한 앵글 감상
- **절대 아닌 것**: 홈페이지, 소개 페이지, About, Footer 같은 웹사이트 요소 불필요
- **디자인 원칙**: 모노톤 흑백, 미니멀, 고급스러움, 사진이 주인공

---

## 기술 스택 & 규칙

### Tailwind CSS v4
- CDN 사용 금지 (프로덕션 경고 발생)
- 반드시 로컬 빌드: `npm run build` 또는 `npm run dev`
- 커스텀 테마는 `src/input.css`의 `@theme` 블록에 정의
- 빌드 결과물: `dist/output.css`
- HTML 수정 후 반드시 `npm run build` 재실행

### 커스텀 컬러 (mono 팔레트)
```
--color-mono-50:  #fafafa
--color-mono-100: #f5f5f5
--color-mono-200: #e5e5e5
--color-mono-300: #d4d4d4
--color-mono-400: #a3a3a3
--color-mono-500: #737373
--color-mono-600: #525252
--color-mono-700: #404040
--color-mono-800: #262626
--color-mono-900: #171717
--color-mono-950: #0a0a0a
```

### 폰트
- 제목/브랜드: `Playfair Display` (serif)
- 본문/UI: `Inter` (sans-serif)
- Google Fonts CDN으로 로드

### JavaScript
- Vanilla JS (프레임워크 없음)
- 모든 JS는 `index.html` 하단 `<script>` 태그 내에 인라인

---

## 핵심 코드 구조

### 드레스 데이터 (`dresses` 배열)
```javascript
const dresses = [
    {
        id: Number,           // 고유 ID
        name: String,         // "Ethereal Veil Gown"
        style: String,        // "Wedding" (표시용)
        category: String,     // "wedding" (필터용: wedding/evening/cocktail/classic)
        thumbnail: String,    // 썸네일 이미지 경로
        images: String[]      // 슬라이드쇼 이미지 배열 (3~4장)
    }
];
```

### 주요 함수
- `buildGrid(filter)` — 필터에 따라 드레스 카드 그리드 생성
- `openSlideshow(dress)` — 특정 드레스의 풀스크린 슬라이드쇼 오픈 (10장)
- `goToSlide(index)` — 특정 슬라이드로 이동
- `updateSlide(animate)` — 슬라이드 전환 (이미지, 썸네일, 카운터, 프로그레스 업데이트)
- `nextSlide()` / `prevSlide()` — 다음/이전 슬라이드
- `toggleAutoplay()` — 자동 재생 토글 (3.5초 간격)
- `closeSlideshow()` — 슬라이드쇼 닫기

### 이벤트 처리
- 키보드: ArrowLeft/Right (탐색), ESC (닫기), Space (자동재생)
- 터치: 좌우 스와이프 60px 이상 → 슬라이드 전환
- 클릭: 카드 클릭 → 슬라이드쇼, 배경 클릭 → 닫기

---

## 이미지 생성 작업 가이드

### 환경 설정
```bash
pip install google-genai
```

### API 키
`.env` 파일에 `GOOGLE_API_KEY` 저장됨

### 이미지 생성 스크립트 작성 시 참고
```python
from google import genai
from google.genai import types
import os

client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

response = client.models.generate_images(
    model="imagen-3.0-generate-002",
    prompt="프롬프트 내용",
    config=types.GenerateImagesConfig(
        number_of_images=1,
        aspect_ratio="3:4",
        output_mime_type="image/png",
    )
)

# 저장
for img in response.generated_images:
    with open("output.png", "wb") as f:
        f.write(img.image.image_bytes)
```

### 드레스별 프롬프트 템플릿

**기본 구조:**
```
A luxurious {style} dress, {description},
displayed on a mannequin in a high-end boutique studio,
soft dramatic lighting, clean black background,
high fashion editorial photography, monochrome aesthetic,
ultra-detailed fabric texture, 8K professional quality
```

**스타일별 키워드:**
- Wedding: white, ivory, tulle, lace, beading, cathedral train, veil
- Evening: satin, silk, floor-length, elegant draping, deep neckline
- Cocktail: knee-length, structured, modern cut, minimal embellishment
- Classic: A-line, timeless silhouette, clean lines, understated elegance

**앵글별 접미사 (10장 구성):**
1. 전면 전신: `front full-length view`
2. 측면: `side profile view, showing the dress silhouette`
3. 후면: `back view, showing zipper and train details`
4. 3/4 앵글: `three-quarter angle view, showing depth and dimension`
5. 디테일 클로즈업: `close-up of bodice / neckline detail`
6. 상체 프레임: `waist-up view, focusing on neckline and shoulders`
7. 로우앵글 / 반대편: `low angle view or opposite side perspective`
8. 부분 디테일: `close-up of waist / hip / hem area detail`
9. 후면 상체: `back upper body detail, closure and strap detail`
10. 극접사: `extreme close-up of fabric texture and embellishments`

### 이미지 저장 구조
```
images/
├── dress-01/
│   ├── thumb.png       (600x800, 썸네일용 = view 1과 동일)
│   ├── view-1.png      (1400px, 전면 전신)
│   ├── view-2.png      (1400px, 측면)
│   ├── view-3.png      (1400px, 후면)
│   ├── view-4.png      (1400px, 3/4 앵글)
│   ├── view-5.png      (1400px, 디테일 클로즈업)
│   ├── view-6.png      (1400px, 상체 프레임)
│   ├── view-7.png      (1400px, 로우앵글/반대편)
│   ├── view-8.png      (1400px, 부분 디테일)
│   ├── view-9.png      (1400px, 후면 상체)
│   └── view-10.png     (1400px, 극접사)
├── dress-02/
│   └── ...
```

### 이미지 생성 후 HTML 업데이트
`dresses` 배열의 URL을 로컬 경로로 교체:
```javascript
{
    id: 1,
    name: "Ethereal Veil Gown",
    style: "Wedding",
    category: "wedding",
    thumbnail: "images/dress-01/thumb.png",
    images: [
        "images/dress-01/view-1.png",
        "images/dress-01/view-2.png",
        "images/dress-01/view-3.png",
        "images/dress-01/view-4.png"
    ]
}
```

---

## 스타일 컨벤션

### CSS 클래스 네이밍
- Tailwind 유틸리티 우선
- 커스텀 클래스는 `<style>` 태그 내에 정의
- 주요 커스텀 클래스: `.dress-card`, `.filter-btn`, `.slide-image`, `.thumb-item`, `.thumb-strip`

### 애니메이션
- 슬라이드 전환: opacity + scale (0.6s cubic-bezier)
- 카드 호버: scale(1.04) (0.8s cubic-bezier)
- 필터 전환: opacity + translateY (0.3s)
- 자동재생 인디케이터: pulse 애니메이션

### 반응형 브레이크포인트
- 기본: 2컬럼 그리드
- md (768px): 3컬럼, 패딩 증가
- lg (1024px): 4컬럼
- 최대 너비: 1600px

---

## 주의사항

1. **Tailwind CDN 절대 사용 금지** — 프로덕션 경고 발생, 반드시 로컬 빌드
2. **이미지 grayscale** — 모든 드레스 이미지에 `grayscale` 클래스 적용 (모노톤 일관성)
3. **홈페이지 요소 금지** — Hero, About, Editorial, Footer 등 불필요
4. **터치 최적화 필수** — 태블릿 사용이 주 목적이므로 터치 이벤트 반드시 처리
5. **이미지 프리로드** — 슬라이드쇼 진입 시 해당 드레스의 모든 이미지를 미리 로드
