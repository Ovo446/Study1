// Word click translation
document.querySelectorAll('.word').forEach(word => {
    word.addEventListener('click', async () => {
        const definition = await fetch(`https://api.dictionaryapi.dev/api/v2/entries/en/${word.textContent}`)
            .then(res => res.json());
        
        // Show definition popup
        const popup = document.createElement('div');
        popup.className = 'definition-popup';
        popup.innerHTML = `
            <h3>${word.textContent}</h3>
            <p>${definition[0].meanings[0].definitions[0].definition}</p>
            <button onclick="addToVocabulary('${word.textContent}')">+ Add to Vocabulary</button>
        `;
        document.body.appendChild(popup);
    });
});

// Text-to-speech
function speakText() {
    const speech = new SpeechSynthesisUtterance();
    speech.text = document.querySelector('.content').textContent;
    window.speechSynthesis.speak(speech);
}

// Add to vocabulary
async function addToVocabulary(word) {
    await fetch('/add-word', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ word })
    });
}
