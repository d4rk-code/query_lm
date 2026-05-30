document.getElementById('chat-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const inputField = document.getElementById('user-query');
    const submitBtn = document.getElementById('submit-btn');
    const queryText = inputField.value.trim();
    if (!queryText) return;

    inputField.disabled = true;
    submitBtn.disabled = true;

    const wrapper = document.getElementById('window-wrapper');
    
    if (wrapper.classList.contains('empty-state')) {
        wrapper.classList.remove('empty-state');
    }

    wrapper.innerHTML = `
        <div class="window-header">
            <span class="dot red"></span><span class="dot yellow"></span><span class="dot green"></span>
            <div class="scanner-container">
                <div class="magnifier">
                    <svg class="lens-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
                    <div class="scanner-beam"></div>
                </div>
            </div>
            <span class="window-title">QUERY LM_ RESPONSE</span>
        </div>
        
        <div class="response-content" id="scroll-target">
            <div class="user-query-box">
                <p class="query-label">YOU</p>
                <p class="query-text" id="stream-question"></p>
            </div>
            <div class="ai-reply-box">
                <p class="query-label ai-label">QUERY LM_</p>
                <div class="markdown-body" id="stream-output"></div>
            </div>
        </div>
    `;

    const scrollTarget = document.getElementById('scroll-target');
    const streamQuestion = document.getElementById('stream-question');
    const streamOutput = document.getElementById('stream-output');

    streamQuestion.textContent = queryText;
    streamOutput.innerHTML = "<p class='loading-text'>Running query on database and generating summary...</p>";
    inputField.value = '';

    try {
        const formData = new FormData();
        formData.append('query', queryText);

        const response = await fetch('/chat', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.status === 'success') {
            // --- SMOOTH TYPING ANIMATION ENGINE ---
            const fullText = data.response;
            let currentLength = 0;
            streamOutput.innerHTML = ""; // Clear loader text

            // Typing loop function
            function typeNextCharacter() {
                if (currentLength <= fullText.length) {
                    // Grab current slice of raw markdown text
                    let partialMarkdown = fullText.substring(0, currentLength);
                    
                    // Convert partial markdown to HTML on the fly so it renders perfectly
                    streamOutput.innerHTML = marked.parse(partialMarkdown);
                    
                    // Increment pacing speed (higher numbers slice more text per tick)
                    currentLength += 3; 
                    
                    // Force the fixed terminal scrollbar downward cleanly as text grows
                    scrollTarget.scrollTop = scrollTarget.scrollHeight;
                    
                    // Run loop at 20ms intervals
                    setTimeout(typeNextCharacter, 20);
                } else {
                    // Final pass to ensure rendering is completely closed out
                    streamOutput.innerHTML = marked.parse(fullText);
                    scrollTarget.scrollTop = scrollTarget.scrollHeight;
                    
                    // Unlock user input forms once typing concludes
                    inputField.disabled = false;
                    submitBtn.disabled = false;
                    inputField.focus();
                }
            }

            // Fire animation engine
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
