const STORAGE_KEY = "query_lm_chat_history";

// FIX: Instead of loading old logs on boot, we clear them instantly on reload!
document.addEventListener("DOMContentLoaded", () => {
    localStorage.removeItem(STORAGE_KEY);
    // The HTML naturally starts in its default welcome/empty-state, so no extra rendering is needed here.
});


// --- THE CHAT HANDLER SUBMIT EVENT ---
document.getElementById('chat-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const inputField = document.getElementById('user-query');
    const submitBtn = document.getElementById('submit-btn');
    const queryText = inputField.value.trim();
    if (!queryText) return;

    inputField.disabled = true;
    submitBtn.disabled = true;

    const wrapper = document.getElementById('window-wrapper');

    // If starting fresh from the welcome state, build the runtime conversation container
    if (wrapper.classList.contains('empty-state') || !document.getElementById('conversation-stream')) {
        wrapper.classList.remove('empty-state');
        wrapper.innerHTML = `
            <div class="window-header">
                <span class="dot red"></span><span class="dot yellow"></span><span class="dot green"></span>
                <div class="scanner-container">
                    <div class="magnifier">
                        <svg class="lens-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
                        <div class="scanner-beam"></div>
                    </div>
                </div>
                <span class="window-title" id="header-title">QUERY LM_ RESPONSE</span>
            </div>
            <div class="response-content" id="scroll-target">
                <div id="conversation-stream"></div>
            </div>
        `;
    }

    const scrollTarget = document.getElementById('scroll-target');
    const streamContainer = document.getElementById('conversation-stream');

    // Generate a unique identifier for the incoming message block
    const uniqueId = "live-run-" + Date.now();
    const hasPriorElements = streamContainer.children.length > 0;
    const optionalBorder = hasPriorElements ? 'style="margin-top: 32px; border-top: 1px dashed #222; padding-top: 24px;"' : '';

    // Append the next question cleanly right onto the existing session stream
    const activeBlock = document.createElement('div');
    activeBlock.innerHTML = `
        <div ${optionalBorder}>
            <div class="user-query-box">
                <p class="query-label">YOU</p>
                <p class="query-text">${escapeHtml(queryText)}</p>
            </div>
            <div class="ai-reply-box">
                <p class="query-label ai-label">QUERY LM_</p>
                <div class="markdown-body" id="${uniqueId}"></div>
            </div>
        </div>
    `;
    streamContainer.appendChild(activeBlock);

    const streamOutput = document.getElementById(uniqueId);
    streamOutput.innerHTML = "<p class='loading-text'>Running query on database and generating summary...</p>";
    inputField.value = '';
    
    // Snaps browser focus down to loading metrics instantly
    scrollTarget.scrollTop = scrollTarget.scrollHeight;

    try {
        const formData = new FormData();
        formData.append('query', queryText);

        const response = await fetch('/chat', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.status === 'success') {
            const fullText = data.response;
            
            // Save the data to local storage so it appends nicely if they ask another question
            saveChatToLocalStorage(queryText, fullText);

            let currentLength = 0;
            streamOutput.innerHTML = "";

            function typeNextCharacter() {
                if (currentLength <= fullText.length) {
                    let partialMarkdown = fullText.substring(0, currentLength);
                    streamOutput.innerHTML = marked.parse(partialMarkdown);
                    currentLength += 3; 
                    scrollTarget.scrollTop = scrollTarget.scrollHeight;
                    setTimeout(typeNextCharacter, 15);
                } else {
                    streamOutput.innerHTML = marked.parse(fullText);
                    scrollTarget.scrollTop = scrollTarget.scrollHeight;
                    
                    inputField.disabled = false;
                    submitBtn.disabled = false;
                    inputField.focus();
                }
            }

            typeNextCharacter();

        } else {
            streamOutput.innerHTML = `<p style="color: #ff5f56;">Error: ${data.message}</p>`;
            inputField.disabled = false;
            submitBtn.disabled = false;
        }

    } catch (err) {
        streamOutput.innerHTML = `<p style="color: #ff5f56;">Execution failure: ${err.message}</p>`;
        inputField.disabled = false;
        submitBtn.disabled = false;
    }
});


// --- SESSION LOCALSTORAGE STORAGE WRITE WORKER ---
function saveChatToLocalStorage(question, response) {
    let currentHistory = [];
    const savedData = localStorage.getItem(STORAGE_KEY);
    
    if (savedData) {
        currentHistory = JSON.parse(savedData);
    }

    currentHistory.push({
        question: question,
        response: response
    });

    localStorage.setItem(STORAGE_KEY, JSON.stringify(currentHistory));
}

function escapeHtml(text) {
    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
