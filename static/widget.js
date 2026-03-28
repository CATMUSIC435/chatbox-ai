(function() {
    const scripts = document.getElementsByTagName('script');
    let API_BASE_URL = "http://127.0.0.1:8000"; // Mặc định
    let customDomain = null;
    const THEME_COLOR = "#2563EB"; // Blue Theme
    
    for(let s of scripts) {
        if(s.src && s.src.includes('widget.js')) {
            try {
                API_BASE_URL = new URL(s.src).origin;
                customDomain = s.getAttribute("data-domain");
            } catch(e) {}
            break;
        }
    }

    const style = document.createElement('style');
    style.innerHTML = `
                #conectai-widget-btn {
            position: fixed; bottom: 20px; right: 20px; width: 80px; height: 80px;
            background: transparent; border-radius: 0;
            display: flex; align-items: center; justify-content: center; 
            cursor: pointer; z-index: 999999;
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        }
        #conectai-widget-btn:hover { transform: scale(1.1) translateY(-5px); }
        #conectai-widget-btn img {
            width: 100%; height: 100%; object-fit: contain; pointer-events: none;
            filter: drop-shadow(0 6px 12px rgba(0,0,0,0.15));
        }
        
                #conectai-widget-panel {
            position: fixed; bottom: 100px; right: 24px; width: 380px; height: 580px; max-height: calc(100vh - 120px);
            background: #ffffff; border-radius: 20px; 
            box-shadow: 0 16px 48px rgba(0,0,0,0.12), 0 0 2px rgba(0,0,0,0.05);
            display: none; flex-direction: column; overflow: hidden; z-index: 999999;
            font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; 
            animation: bottomUp 0.4s cubic-bezier(0.16, 1, 0.3, 1);
            border: 1px solid rgba(0,0,0,0.05);
        }
        @keyframes bottomUp { 
            0% { opacity: 0; transform: translateY(30px) scale(0.95); } 
            100% { opacity: 1; transform: translateY(0) scale(1); } 
        }
        
                #conectai-panel-header {
            background: linear-gradient(135deg, ${THEME_COLOR} 0%, #1e40af 100%); 
            color: white; padding: 18px 20px; font-weight: 600;
            display: flex; justify-content: space-between; align-items: center;
        }
        .conectai-bot-avatar { 
            background: rgba(255,255,255,0.2); backdrop-filter: blur(4px);
            padding: 6px 14px; border-radius: 20px; font-size: 14px; letter-spacing: 0.3px;
            display: flex; align-items: center; gap: 6px;
        }
        #conectai-close-btn { 
            cursor: pointer; font-size: 20px; opacity: 0.7; transition: 0.2s;
            display: flex; justify-content: center; align-items: center; width: 32px; height: 32px; border-radius: 50%;
        }
        #conectai-close-btn:hover { opacity: 1; background: rgba(255,255,255,0.15); }
        
                #conectai-chat-body {
            flex-grow: 1; padding: 20px; overflow-y: auto; background: #fdfdfd;
            display: flex; flex-direction: column; gap: 18px; scroll-behavior: smooth;
        }
        
                .conectai-msg { max-width: 85%; padding: 14px 18px; font-size: 14.5px; line-height: 1.5; word-wrap: break-word; animation: fadeIn 0.3s ease; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(5px); } to { opacity:1; transform: translateY(0); } }
        
        .conectai-msg.user { 
            background: linear-gradient(135deg, ${THEME_COLOR}, #1e40af); color: white; align-self: flex-end; 
            border-radius: 20px 20px 4px 20px; box-shadow: 0 4px 12px rgba(37,99,235,0.18); 
        }
        .conectai-msg.bot { 
            background: #ffffff; color: #1f2937; align-self: flex-start; 
            border-radius: 20px 20px 20px 4px; box-shadow: 0 4px 16px rgba(0,0,0,0.06); border: 1px solid #f3f4f6; 
        }
        
                #conectai-input-area {
            display: flex; padding: 16px; background: white; gap: 12px;
            border-top: 1px solid #f3f4f6; align-items: center;
        }
        #conectai-input {
            flex-grow: 1; border: 1px solid transparent; padding: 14px 18px;
            border-radius: 24px; outline: none; font-size: 14.5px; background: #f3f4f6;
            transition: all 0.3s ease; color: #1f2937;
        }
        #conectai-input:focus { border-color: rgba(37,99,235,0.3); background: #ffffff; box-shadow: 0 0 0 3px rgba(37,99,235,0.1); }
        #conectai-input::placeholder { color: #9ca3af; }
        
        #conectai-send-btn {
            background: linear-gradient(135deg, ${THEME_COLOR}, #1e40af); color: white; border: none; 
            width: 46px; height: 46px; min-width: 46px;
            border-radius: 50%; cursor: pointer; display: flex; align-items: center; justify-content: center;
            transition: all 0.3s ease; box-shadow: 0 4px 12px rgba(37,99,235,0.25);
        }
        #conectai-send-btn:hover { transform: scale(1.08) rotate(5deg); box-shadow: 0 6px 16px rgba(37,99,235,0.35); }
        #conectai-send-btn svg { width: 18px; height: 18px; fill: white; margin-left: 2px;}
        
                .conectai-sugg-container { display: flex; flex-direction: column; gap: 8px; margin-top: 4px; max-width: 90%; align-self: flex-start;}
        .conectai-sugg-btn { 
            background: #ffffff; border: 1px solid #e5e7eb; color: ${THEME_COLOR}; 
            padding: 10px 14px; border-radius: 16px; font-size: 13.5px; cursor: pointer; font-weight: 500;
            transition: all 0.25s ease; text-align: left; box-shadow: 0 2px 6px rgba(0,0,0,0.03);
            display: flex; align-items: center; gap: 8px;
        }
        .conectai-sugg-btn:hover { background: #eff6ff; border-color: ${THEME_COLOR}; transform: translateX(4px); box-shadow: 0 4px 8px rgba(37,99,235,0.1);}
    `;
    document.head.appendChild(style);
    const btn = document.createElement('div');
    btn.id = 'conectai-widget-btn';
    btn.innerHTML = `<img src="${API_BASE_URL}/static/ai-chatbot.gif" alt="Chat">`;
    document.body.appendChild(btn);

    const panel = document.createElement('div');
    panel.id = 'conectai-widget-panel';
    const sendIcon = `<svg viewBox="0 0 24 24"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"></path></svg>`;
    
    panel.innerHTML = `
        <div id="conectai-panel-header">
            <span class="conectai-bot-avatar">
                <img src="${API_BASE_URL}/static/ai-chatbot.gif" style="width: 22px; height: 22px; border-radius: 50%; border: 1px solid rgba(255,255,255,0.4);" alt="Bot">
                ConectAI
            </span>
            <span id="conectai-close-btn">✖</span>
        </div>
        <div id="conectai-chat-body">
            <div class="conectai-msg bot">Chào bạn! Mình có thể hỗ trợ tư vấn thông tin gì cho bạn?</div>
        </div>
        <div id="conectai-input-area">
            <input type="text" id="conectai-input" placeholder="Nhập câu hỏi tại đây..." autocomplete="off">
            <button id="conectai-send-btn">${sendIcon}</button>
        </div>
    `;
    document.body.appendChild(panel);
    let isOpen = false;
    btn.onclick = () => {
        isOpen = !isOpen;
        panel.style.display = isOpen ? 'flex' : 'none';
        
        if (isOpen) {
            document.getElementById('conectai-input').focus();
        }
    };
    document.getElementById('conectai-close-btn').onclick = () => btn.click();
    const chatBody = document.getElementById('conectai-chat-body');
    const inputField = document.getElementById('conectai-input');
    const sendBtn = document.getElementById('conectai-send-btn');

    inputField.addEventListener("keypress", (e) => {
        if(e.key === 'Enter') window.conectaiSendMsg();
    });
    sendBtn.onclick = () => window.conectaiSendMsg();

    window.conectaiSendMsg = async function(presetText = null) {
        const text = presetText !== null ? presetText : inputField.value.trim();
        if(!text) return;
        inputField.value = '';
        document.querySelectorAll('.conectai-sugg-container').forEach(el => el.remove());
        const userMsg = document.createElement('div');
        userMsg.className = 'conectai-msg user';
        userMsg.innerText = text;
        chatBody.appendChild(userMsg);
        chatBody.scrollTop = chatBody.scrollHeight;
        const botMsg = document.createElement('div');
        botMsg.className = 'conectai-msg bot';
        botMsg.innerHTML = '<span style="opacity:0.5">Đang suy nghĩ...</span>';
        chatBody.appendChild(botMsg);
        chatBody.scrollTop = chatBody.scrollHeight;

        try {
            const currentDomain = customDomain || window.location.hostname || "default";

            const res = await fetch(`${API_BASE_URL}/chat-stream`, {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({ question: text, domain: currentDomain })
            });

            if (!res.ok) throw new Error("Server trả về lỗi " + res.status);
            
            const reader = res.body.getReader();
            const decoder = new TextDecoder("utf-8");
            botMsg.innerText = ""; // Xóa chữ Đang suy nghĩ
            
            while (true) {
                const { value, done } = await reader.read();
                if (done) break;
                botMsg.innerText += decoder.decode(value, { stream: true });
                chatBody.scrollTop = chatBody.scrollHeight;
            }
            const fullText = botMsg.innerText;
            const match = fullText.match(/\[SUGGESTIONS\]|---SUGGESTIONS---|SUGGESTIONS:?/i);
            
            if (match) {
                const suggestIndex = match.index;
                botMsg.innerText = fullText.substring(0, suggestIndex).trim();
                const suggestionsStr = fullText.substring(suggestIndex + match[0].length).trim();
                let questions = [];
                if (suggestionsStr.includes('|')) {
                    questions = suggestionsStr.split('|');
                } else {
                    questions = suggestionsStr.split('\n');
                }
                questions = questions
                    .map(q => q.replace(/^[-\*\d\.\s]+/, '').replace(/^["']|["']$/g, '').trim())
                    .filter(q => q.length > 5); // Bỏ các câu quá ngắn
                    
                if(questions.length > 0) {
                    const sugContainer = document.createElement('div');
                    sugContainer.className = 'conectai-sugg-container';
                    
                    questions.slice(0, 3).forEach(q => {
                        const sugBtn = document.createElement('div');
                        sugBtn.className = 'conectai-sugg-btn';
                        sugBtn.innerText = "✨ " + q;
                        sugBtn.onclick = () => window.conectaiSendMsg(q);
                        sugContainer.appendChild(sugBtn);
                    });
                    
                    chatBody.appendChild(sugContainer);
                    chatBody.scrollTop = chatBody.scrollHeight;
                }
            }
        } catch(e) {
            botMsg.innerText = "❌ Không thể kết nối tới Trợ lý AI: " + e.message;
        }
        chatBody.scrollTop = chatBody.scrollHeight;
    }
})();
