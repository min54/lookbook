# 배포 가이드 — GitHub + Netlify

## 1. GitHub 레포 생성 & 푸시

```bash
# lookbook 폴더에서 실행
cd lookbook

# git 초기화 (이미 안 되어 있다면)
git init -b main
git config user.email "kataroteno@gmail.com"
git config user.name "min byoung"

# .env는 커밋하지 않음 (.gitignore에 포함됨)
git add .gitignore PROJECT.md SKILL.md DEPLOY.md generate_images.py index.html package.json package-lock.json src/input.css
git commit -m "Initial commit: MONO Dress Shop Digital Lookbook"

# GitHub 레포 생성 (gh CLI 필요)
gh repo create mono-dress-lookbook --public --source=. --remote=origin --push

# 또는 수동으로:
# 1. GitHub에서 'mono-dress-lookbook' 레포 생성
# 2. git remote add origin https://github.com/YOUR_USERNAME/mono-dress-lookbook.git
# 3. git push -u origin main
```

## 2. Netlify 배포

### 방법 A: Netlify CLI (추천)

```bash
# Netlify CLI 설치
npm install -g netlify-cli

# 로그인 (min54 계정)
netlify login

# 새 사이트 생성 & 배포
# dist 대신 루트(.) 를 배포 (index.html이 루트에 있으므로)
netlify deploy --prod --dir=.

# 또는 GitHub 연동 자동 배포
netlify init
```

### 방법 B: Netlify 웹 대시보드

1. https://app.netlify.com 접속 (min54 계정)
2. "Add new site" → "Import an existing project"
3. GitHub 연결 → `mono-dress-lookbook` 레포 선택
4. Build settings:
   - Build command: `npm run build`
   - Publish directory: `.` (루트)
5. "Deploy site" 클릭

### 방법 C: 드래그 & 드롭

1. https://app.netlify.com/drop 접속
2. lookbook 폴더에서 아래 파일들을 드래그:
   - `index.html`
   - `dist/` 폴더 (output.css 포함)
3. 자동 배포 완료

## 3. Netlify 빌드 설정 (GitHub 연동 시)

`netlify.toml` 파일을 루트에 추가:

```toml
[build]
  command = "npm run build"
  publish = "."

[build.environment]
  NODE_VERSION = "18"
```

## 4. 커스텀 도메인 (선택)

Netlify 대시보드 → Site settings → Domain management
- 기본: `xxx.netlify.app`
- 커스텀: 원하는 도메인 연결 가능
