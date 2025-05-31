# 🛒 Smart Shopper Frontend

> **AI 기반 스마트 쇼핑 도우미의 프론트엔드 구현**  
> 실시간 가격 비교 및 가성비 분석을 제공하는 채팅 인터페이스

## 📋 프로젝트 개요

### 🎯 목표
- 실시간 가격 정보와 가성비 분석을 제공하여 현명한 소비 지원
- 마트별 할인 정보를 제공하여 사용자 선택의 폭 확대

### 💡 배경
소비자가 마트에서 상품을 구입할 때, 동일 상품에 대한 다른 마트의 가격 정보를 알지 못하여 해당 상품의 가격이 적절한지, 합리적인 소비인지 판단하기 어려운 문제를 해결하고자 했다.

### ⚡ 주요 기능
- 실시간 가격 비교 및 가성비 평가
- 특정 상품 가격 입력/검색 시 최적 가격과 가성비 분석 결과 제공
- 마트별 할인 정보 제공
- 개인 맞춤형 추천

## 🛠 기술 스택

### Frontend
- HTML5
- CSS3
- JavaScript
- Tailwind CSS

### Libraries & APIs
- **Marked.js** - 마크다운 파싱 라이브러리
- **Fetch API** - 네이티브 비동기 통신

### Build & Deploy
- Parcel
- Vercel
- GitHub Actions

## 🎯 기술 선택 이유

### **JavaScript**
- 빠른 로딩 속도 확보
- 가벼운 번들 사이즈로 성능 최적화

### **Marked.js**
- 경량화된 마크다운 파서로 AI 응답의 풍부한 텍스트 표현 지원
- 작은 용량으로 성능에 미치는 영향 최소화

### **Fetch API**
- 네이티브 비동기 통신으로 외부 라이브러리 의존성 최소화
- Promise 기반의 직관적인 비동기 처리

## 🚀 핵심 구현 기능

### 1. **실시간 채팅 인터페이스**
```javascript
// 동적 메시지 버블 생성
function createMessageBubble(content, sender = "user") {
  // DOM 조작을 통한 효율적인 메시지 렌더링 시스템
}

// 자동 스크롤 구현
function scrollToBottom() {
  chatContainer.scrollTo({
    top: scrollHeight,
    behavior: 'smooth'
  });
}
```

**주요 특징:**
- 메시지 전송/수신, 로딩 상태 표시, 자동 스크롤
- Enter 키 전송, Shift + Enter로 줄바꿈
- 새 메시지 입력 시 하단으로 자동 이동

### 2. **마크다운 렌더링 시스템**
```javascript
// 마크다운 파싱 및 렌더링
if (content.includes('#') || content.includes('*') || content.includes('`')) {
  bubble.innerHTML = marked.parse(content, {
    breaks: true,
    gfm: true
  });
}
```

AI 응답의 헤더, 리스트, 코드 블록 등 마크다운 형식을 채팅 UI에 최적화하여 지원

### 3. **반응형 UI 시스템**
```css
/* 반응형 브레이크포인트 */
@media (max-width: 1024px) { --side-padding: 2rem; }
@media (max-width: 768px) { --side-padding: 1rem; }
```

모바일부터 데스크톱까지 최적화된 UI 제공

### 4. **텍스트 입력창 자동 높이 조절**
```javascript
textarea.addEventListener("input", function() {
  this.style.height = "24px";
  const newHeight = Math.min(this.scrollHeight, 200);
  this.style.height = newHeight + "px";
});
```

사용자 입력에 따른 실시간 UI 반응으로 사용성 향상

### 5. **CSS 애니메이션 구현**
```css
@keyframes bounce {
  0% { transform: translateY(0); }
  100% { transform: translateY(-10px); }
}

.loading-dots span {
  animation: bounce 0.6s infinite alternate;
}
```

AI 응답 로딩 시 점 3개 바운스 효과를 통한 시각적 피드백 제공

### 6. **비동기 통신 시스템**
```javascript
async function getAssistantResponse(userMessage) {
  const response = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: userMessage }),
  });
  return await response.json();
}
```

Fetch API와 Promise 패턴을 활용한 서버 통신 및 실시간 로딩 상태 표시

## 🔧 문제 해결 사례

### **마크다운 여백 최적화 문제**

**🚨 문제 상황**
- AI 챗봇 응답의 마크다운 형식 적용 시 불필요하게 큰 여백들이 생성
- 브라우저 기본 HTML 요소들(h1, h2, p, ul 등)의 상하 마진(1em)이 마크다운 파싱 시 합쳐져 과도한 공백 발생

**💡 해결 방법**
```css
/* 마크다운 요소 마진 최적화 */
.assistant-message h1, h2, h3, h4, h5, h6 {
  margin: 0.2em 0 0em 0;  /* 기본 1em → 0.2em */
}

.assistant-message p {
  margin: 0.3em 0;        /* 기본 1em → 0.3em */
}

.assistant-message ul, ol {
  margin: 0.1em 0;        /* 기본 1em → 0.1em */
}

/* 헤더 다음 요소 간격 특별 처리 */
.assistant-message h1 + *, h2 + *, h3 + * {
  margin-top: 0.05em !important;
}
```

**📈 결과**
- 기존 32px 간격 → 3-5px로 대폭 축소
- 채팅 UI에 적합한 자연스러운 간격 구현
- 사용자 가독성 향상

## 📁 프로젝트 구조

```
frontend/
├── src/
│   ├── styles.css      # 커스텀 CSS (채팅 특화 스타일)
│   └── app.js          # 메인 JavaScript 로직
├── index.html          # 메인 HTML (Tailwind 클래스 포함)
├── package.json        # 의존성 및 빌드 스크립트
├── tailwind.config.js  # Tailwind 설정
└── .postcssrc.json     # PostCSS 설정
```

## 🚀 개발 환경 설정

```bash
# 의존성 설치
npm install

# 개발 서버 실행
npm start
```

## 📊 프로젝트 성과

### ✅ **기술적 성과**
- **성능 최적화**: 가벼운 번들 사이즈와 빠른 로딩 속도
- **마크다운 렌더링 최적화**: CSS 마진 조정을 통해 32px → 3-5px로 여백 축소, 채팅 UI에 최적화된 마크다운 표시
- **동적 UI 구현**: 텍스트 입력창 자동 높이 조절(최대 200px) 및 실시간 반응형 인터페이스

### ✅ **사용자 경험 개선**
- **일관된 반응형 UI**: 모바일/태블릿/데스크톱 등 다양한 환경에서 최적화
- **가독성 향상**: 마크다운 지원으로 AI 응답에 대한 가독성을 높임
- **최적화된 마크다운 표시**: CSS 여백 조정으로 채팅 환경에 적합한 자연스러운 간격 구현
- **끊김 없는 UX**: 비동기 처리로 AI 응답 대기 중에도 자유로운 화면 조작

## 🔗 관련 링크

- **Live Demo**: [Vercel 배포 사이트](https://ai-frontend-gold.vercel.app/)

---