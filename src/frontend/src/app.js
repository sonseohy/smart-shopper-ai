const chatContainer = document.getElementById("chat-container");
const messageForm = document.getElementById("message-form");
const userInput = document.getElementById("user-input");
const initialMessage = document.getElementById("initial-message");
const textarea = document.getElementById("user-input");

function createMessageBubble(content, sender = "user") {
  const wrapper = document.createElement("div");
  wrapper.classList.add("message-wrapper");

  const avatar = document.createElement("div");
  
  if (sender === "assistant") {
    avatar.classList.add("avatar-assistant");
  }

  const bubble = document.createElement("div");
  bubble.classList.add("message-bubble");

  if (sender === "assistant") {
    bubble.classList.add("assistant-message");
    // 마크다운 파싱 전에 마크다운 문법이 있는지 확인
    if (content.includes('#') || 
        content.includes('*') || 
        content.includes('`') || 
        content.includes('-') || 
        content.includes('1.') ||
        content.includes('[')) {
      // 마크다운이 있는 경우만 marked.parse 사용
      bubble.innerHTML = marked.parse(content, {
        breaks: true,
        gfm: true
      });
    } else {
      // 마크다운이 없는 경우 일반 텍스트로 처리
      bubble.textContent = content;
    }
  } else {
    bubble.classList.add("user-message");
    bubble.textContent = content;
  }

  if (sender === "assistant") {
    wrapper.appendChild(avatar);
  }
  wrapper.appendChild(bubble);
  return wrapper;
}

// 하단 스크롤
function scrollToBottom() {
  const scrollHeight = chatContainer.scrollHeight;
  chatContainer.scrollTo({
    top: scrollHeight,
    behavior: 'smooth'
  });
}

async function getAssistantResponse(userMessage) {
  const url = "https://ssafy-2024-backend-gwangju-3.fly.dev/assistant";

  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message: userMessage }),
  });

  if (!response.ok) {
    throw new Error("Network response was not ok");
  }

  const data = await response.json();
  return data.reply;
}

// 로딩중 표시 추가
function addLoadingDots() {
  const loadingDiv = document.createElement("div");
  loadingDiv.classList.add("loading-dots");
  loadingDiv.innerHTML = '<span>.</span><span>.</span><span>.</span>';
  chatContainer.appendChild(loadingDiv);
  scrollToBottom();
}

// 로딩중 표시 제거
function removeLoadingDots() {
  const loadingDiv = document.querySelector(".loading-dots");
  if (loadingDiv) {
    loadingDiv.remove();
  }
}

messageForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const message = userInput.value.trim();
  if (!message) return;

  // 초기 메시지 제거
  if (initialMessage) {
    initialMessage.remove();
  }

  // 사용자 메시지
  chatContainer.appendChild(createMessageBubble(message, "user"));
  userInput.value = "";

  // 입력창 높이 초기화
  textarea.style.height = "24px"; // 기본 높이로 리셋

  scrollToBottom();

  // 로딩 중 표시 추가
  addLoadingDots();

  try {
    const response = await getAssistantResponse(message);
    chatContainer.appendChild(createMessageBubble(response, "assistant"));
    removeLoadingDots();  // 로딩 중 표시 제거
    scrollToBottom();
  } catch (error) {
    console.error("Error fetching assistant response:", error);
    chatContainer.appendChild(
      createMessageBubble(
        "Error fetching response. Check console.",
        "assistant"
      )
    );
    removeLoadingDots();  // 로딩 중 표시 제거
    scrollToBottom();
  }
});

// 입력창 자동 리사이징
textarea.addEventListener("keydown", function(e) {
  if (e.key === "Enter") {
    if (!e.shiftKey) {
      e.preventDefault();
      // 내용이 있을 때만 전송
      if (this.value.trim()) {
        messageForm.dispatchEvent(new Event("submit"));
      }
    }
  }
});

// 자동 높이 조절
textarea.addEventListener("input", function() {
  this.style.height = "24px";
  const newHeight = Math.min(this.scrollHeight, 200);
  this.style.height = newHeight + "px";
  scrollToBottom();
});

// 로고 클릭 시 페이지 새로고침
document.getElementById('logo').addEventListener('click', function() {
  location.reload();  // 페이지 새로고침
});
