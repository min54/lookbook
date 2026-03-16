"""
MONO Dress Lookbook — 드레스 이미지 자동 생성 스크립트
Google Gemini Imagen 3 API 사용

사용법:
    1. .env 파일에 GOOGLE_API_KEY 설정
    2. pip install google-genai python-dotenv
    3. python generate_images.py
"""

import os
import sys
import time
from pathlib import Path

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("ERROR: google-genai 패키지가 필요합니다.")
    print("설치: pip install google-genai")
    sys.exit(1)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv 없으면 환경변수에서 직접 읽음

# ===== 설정 =====
API_KEY = os.environ.get("GOOGLE_API_KEY", "")
MODEL = "imagen-3.0-generate-002"
ASPECT_RATIO = "3:4"
OUTPUT_DIR = Path("images")
THUMB_SUFFIX = "thumb"

if not API_KEY:
    print("ERROR: GOOGLE_API_KEY가 설정되지 않았습니다.")
    print(".env 파일 또는 환경변수에 키를 설정해주세요.")
    sys.exit(1)

client = genai.Client(api_key=API_KEY)

# ===== 드레스 정의 =====
# 각 드레스별 프롬프트 (스타일, 설명, 앵글별 추가 프롬프트)
DRESSES = [
    {
        "id": "dress-01",
        "name": "Ethereal Veil Gown",
        "category": "wedding",
        "base_prompt": "A luxurious white wedding gown with delicate tulle layers and subtle beading, displayed on a mannequin",
        "views": [
            "front full-length view, showing the complete silhouette",
            "side profile view, showing the flowing tulle train",
            "back view, showing the open back with delicate lace details",
            "three-quarter angle view from the left, showing depth and dimension",
            "close-up of the bodice, showing intricate beadwork and fabric texture",
            "waist-up front view, focusing on the neckline and shoulders",
            "low angle full-length view, dramatic perspective looking up",
            "close-up of the tulle skirt layers and hem detail",
            "back upper body detail, showing the lace closure and buttons",
            "extreme close-up of the beading and crystal embellishments",
        ]
    },
    {
        "id": "dress-02",
        "name": "Midnight Satin Dress",
        "category": "evening",
        "base_prompt": "A sleek black satin evening gown with elegant draping and a deep V-neckline, displayed on a mannequin",
        "views": [
            "front full-length view, dramatic lighting on the satin fabric",
            "side profile view, showing the body-hugging silhouette",
            "back view, showing the low back and train",
            "three-quarter angle from the right, showing the draping",
            "close-up detail of the satin fabric sheen and draping",
            "waist-up view, focusing on the deep V-neckline",
            "full-length view from slight angle, showing movement in fabric",
            "close-up of the hip area, showing the satin gathering detail",
            "back upper body, showing the strap detail and skin reveal",
            "extreme close-up of the satin fabric texture and light reflection",
        ]
    },
    {
        "id": "dress-03",
        "name": "Pearl Lace Bridal",
        "category": "wedding",
        "base_prompt": "An ivory bridal gown with all-over French lace and pearl embellishments, displayed on a mannequin",
        "views": [
            "front full-length view, showing the lace overlay",
            "side view, showing the mermaid silhouette with lace train",
            "back view, showing buttons down the spine and chapel train",
            "three-quarter angle, showing the fitted bodice and flared skirt",
            "extreme close-up of the pearl and lace embroidery details",
            "waist-up front view, showing the sweetheart neckline under lace",
            "full-length back view from slight angle, showing the train spread",
            "close-up of the sleeve lace pattern and scalloped edge",
            "detail shot of the button row down the back",
            "extreme close-up of individual pearl clusters on lace",
        ]
    },
    {
        "id": "dress-04",
        "name": "Noir Velvet Cocktail",
        "category": "cocktail",
        "base_prompt": "A black velvet cocktail dress, knee-length with a structured bodice and clean modern lines, displayed on a mannequin",
        "views": [
            "front full-length view, showing the structured silhouette",
            "side profile view, showing the fitted waist and flared skirt",
            "back view, showing the clean zipper line and back neckline",
            "three-quarter angle, dramatic shadow play on the velvet",
            "close-up of the velvet texture and neckline detail",
            "waist-up view, showing the structured bodice construction",
            "low angle view, showing the hemline and skirt movement",
            "close-up of the waist seam and construction detail",
            "back upper body, showing the neckline from behind",
            "extreme close-up of the velvet pile texture under light",
        ]
    },
    {
        "id": "dress-05",
        "name": "Ivory Draped Gown",
        "category": "evening",
        "base_prompt": "An ivory Grecian-style evening gown with soft draped fabric and one-shoulder design, displayed on a mannequin",
        "views": [
            "front full-length view, showing the flowing draped fabric",
            "side view, showing the asymmetric shoulder and movement",
            "back view, showing the open back with gathered fabric",
            "three-quarter angle from the draped shoulder side",
            "close-up of the shoulder draping and fabric texture",
            "waist-up view, showing the one-shoulder design detail",
            "full-length from opposite side, showing the bare shoulder",
            "close-up of the waist gathering and fabric folds",
            "back detail, showing the cross-draping at the spine",
            "extreme close-up of the chiffon fabric weave and drape",
        ]
    },
    {
        "id": "dress-06",
        "name": "Chiffon Flow Dress",
        "category": "classic",
        "base_prompt": "A white chiffon A-line dress with a delicate sweetheart neckline and soft flowing skirt, displayed on a mannequin",
        "views": [
            "front full-length view, soft ethereal lighting",
            "side view, showing the graceful A-line silhouette",
            "back view, showing the delicate back closure",
            "three-quarter angle, showing the chiffon layers floating",
            "close-up of the sweetheart neckline and chiffon layers",
            "waist-up view, showing bodice ruching detail",
            "full-length with slight wind effect on the chiffon skirt",
            "close-up of the skirt hem and chiffon movement",
            "back upper body, showing the zipper and fabric gathering",
            "extreme close-up of the chiffon fabric transparency and layers",
        ]
    },
    {
        "id": "dress-07",
        "name": "Silhouette A-Line",
        "category": "classic",
        "base_prompt": "A timeless off-white A-line dress with clean architectural lines and minimal embellishment, displayed on a mannequin",
        "views": [
            "front full-length view, crisp clean lines",
            "side profile, showing the perfect A-line shape",
            "back view, showing the elegant zipper line and structure",
            "three-quarter angle, showing the architectural form",
            "close-up of the fabric weave and construction details",
            "waist-up view, showing the clean neckline and shoulders",
            "low angle view emphasizing the A-line flare",
            "close-up of the waist seam and dart construction",
            "back lower body, showing the skirt structure and hem",
            "extreme close-up of the premium fabric texture",
        ]
    },
    {
        "id": "dress-08",
        "name": "Sequin Evening Gown",
        "category": "evening",
        "base_prompt": "A silver sequin floor-length evening gown that catches light beautifully, form-fitting with a mermaid tail, displayed on a mannequin",
        "views": [
            "front full-length view, sequins catching dramatic light",
            "side profile, showing the mermaid silhouette",
            "back view, showing the sequin pattern down the spine",
            "three-quarter angle, light sparkling across the sequins",
            "close-up of the sequin pattern and reflections",
            "waist-up view, showing the neckline and sequin coverage",
            "full-length from slight angle, showing the mermaid flare",
            "close-up of the hip area where mermaid flare begins",
            "back detail of the zipper concealed under sequins",
            "extreme close-up of individual sequins and their arrangement",
        ]
    },
    {
        "id": "dress-09",
        "name": "Tulle Dream Bridal",
        "category": "wedding",
        "base_prompt": "A romantic blush-tinted wedding gown with layers of soft tulle and a princess ball gown skirt, displayed on a mannequin",
        "views": [
            "front full-length view, voluminous tulle skirt",
            "side view, showing the dramatic ball gown volume",
            "back view, showing the lace-up corset back and tulle layers",
            "three-quarter angle, showing the full princess silhouette",
            "close-up of the corset bodice and tulle texture",
            "waist-up view, showing the sweetheart bodice with blush tint",
            "low angle view emphasizing the massive tulle skirt volume",
            "close-up of the tulle layers and their blush color gradient",
            "back corset detail, showing the ribbon lacing",
            "extreme close-up of the tulle fabric and any sparkle elements",
        ]
    },
    {
        "id": "dress-10",
        "name": "Minimalist Slip Dress",
        "category": "cocktail",
        "base_prompt": "A minimalist white silk slip dress with thin straps and a cowl neckline, mid-length, displayed on a mannequin",
        "views": [
            "front full-length view, clean minimal aesthetic",
            "side profile, showing the relaxed elegant silhouette",
            "back view, showing the simple open back and thin straps",
            "three-quarter angle, showing the cowl neckline depth",
            "close-up of the cowl neckline and silk fabric",
            "waist-up view, showing the strap detail and neckline",
            "full-length from behind at angle, showing the back drape",
            "close-up of the thin strap construction and attachment",
            "detail of the hemline and silk weight at the bottom",
            "extreme close-up of the silk fabric sheen and texture",
        ]
    },
    {
        "id": "dress-11",
        "name": "Grace Column Gown",
        "category": "classic",
        "base_prompt": "An elegant white column gown with a high neckline and sleek vertical lines, inspired by classic Hollywood glamour, displayed on a mannequin",
        "views": [
            "front full-length view, elongating vertical lines",
            "side view, showing the sleek column shape",
            "back view, showing the dramatic low back contrast",
            "three-quarter angle, showing the column form elegance",
            "close-up of the high neckline and fabric draping",
            "waist-up view, showing the high neck and shoulder line",
            "full-length from behind, showing the low back reveal",
            "close-up of the waist area, showing the columnar fall of fabric",
            "back neckline detail, showing the contrast of high front low back",
            "extreme close-up of the fabric quality and clean finish",
        ]
    },
    {
        "id": "dress-12",
        "name": "Embroidered Cocktail",
        "category": "cocktail",
        "base_prompt": "A white cocktail dress with delicate floral embroidery and a fit-and-flare shape, above the knee, displayed on a mannequin",
        "views": [
            "front full-length view, showing embroidery pattern",
            "side profile, showing the fit-and-flare shape",
            "back view, showing the embroidery continuation on the back",
            "three-quarter angle, showing the flare movement",
            "extreme close-up of the floral embroidery detail work",
            "waist-up view, showing the embroidery on the bodice",
            "low angle view, showing the flared skirt hemline",
            "close-up of the waist transition from fitted to flared",
            "back upper body, showing the embroidery pattern from behind",
            "extreme close-up of thread colors and embroidery craftsmanship",
        ]
    },
]

STYLE_SUFFIX = (
    "in a high-end boutique studio, soft dramatic lighting, "
    "clean dark background, high fashion editorial photography, "
    "monochrome aesthetic, ultra-detailed, 8K professional quality"
)


def generate_dress_images():
    """모든 드레스의 이미지를 생성합니다."""
    total_images = sum(len(d["views"]) for d in DRESSES)
    generated = 0
    failed = 0

    print(f"\n{'='*60}")
    print(f"  MONO Dress Lookbook — 이미지 생성")
    print(f"  총 {len(DRESSES)}벌, {total_images}장 생성 예정")
    print(f"{'='*60}\n")

    for dress in DRESSES:
        dress_dir = OUTPUT_DIR / dress["id"]
        dress_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n▸ [{dress['id']}] {dress['name']} ({dress['category']})")

        for i, view_prompt in enumerate(dress["views"]):
            filename = f"view-{i+1}.png" if i > 0 else "thumb.png"
            filepath = dress_dir / filename

            # 이미 생성된 파일은 건너뛰기
            if filepath.exists():
                print(f"  ✓ {filename} (이미 존재, 건너뜀)")
                generated += 1
                continue

            full_prompt = f"{dress['base_prompt']}, {view_prompt}, {STYLE_SUFFIX}"

            try:
                print(f"  ⏳ {filename} 생성 중...", end="", flush=True)

                response = client.models.generate_images(
                    model=MODEL,
                    prompt=full_prompt,
                    config=types.GenerateImagesConfig(
                        number_of_images=1,
                        aspect_ratio=ASPECT_RATIO,
                        output_mime_type="image/png",
                    )
                )

                if response.generated_images:
                    img_bytes = response.generated_images[0].image.image_bytes
                    with open(filepath, "wb") as f:
                        f.write(img_bytes)
                    size_kb = len(img_bytes) / 1024
                    print(f" ✅ ({size_kb:.0f}KB)")
                    generated += 1
                else:
                    print(f" ❌ 이미지 생성 실패")
                    failed += 1

                # API 속도 제한 방지
                time.sleep(2)

            except Exception as e:
                print(f" ❌ 에러: {e}")
                failed += 1
                time.sleep(3)

    print(f"\n{'='*60}")
    print(f"  완료! 성공: {generated}장 / 실패: {failed}장")
    print(f"  이미지 경로: {OUTPUT_DIR.absolute()}")
    print(f"{'='*60}\n")

    if generated > 0:
        print("다음 단계: index.html의 dresses 배열에서")
        print("Unsplash URL을 로컬 이미지 경로로 교체하세요.")
        print("예: 'images/dress-01/thumb.png'")


def generate_single(dress_id: str):
    """특정 드레스 하나만 생성합니다."""
    dress = next((d for d in DRESSES if d["id"] == dress_id), None)
    if not dress:
        print(f"ERROR: '{dress_id}' 드레스를 찾을 수 없습니다.")
        print(f"가능한 ID: {', '.join(d['id'] for d in DRESSES)}")
        return

    DRESSES_TEMP = DRESSES.copy()
    DRESSES.clear()
    DRESSES.append(dress)
    generate_dress_images()
    DRESSES.clear()
    DRESSES.extend(DRESSES_TEMP)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # 특정 드레스만 생성: python generate_images.py dress-01
        generate_single(sys.argv[1])
    else:
        # 전체 생성
        generate_dress_images()
