document.getElementById('play-audio-btn').addEventListener('click', async () => {
    const simplifiedText = document.querySelector('#welcome-area p').innerText; // Get the simplified text

    if (!simplifiedText) {
        alert('No simplified text available to play.');
        return;
    }

    try {
        // Fetch the audio file from the backend
        const response = await fetch('/image/get-audio', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ simplified_text: simplifiedText })
        });

        if (response.ok) {
            const audioBlob = await response.blob();
            const audioUrl = URL.createObjectURL(audioBlob);

            // Set the audio source and show the player
            const audioPlayer = document.getElementById('audio-player');
            audioPlayer.src = audioUrl;
            audioPlayer.style.display = 'block';
            audioPlayer.play();
        } else {
            alert('Failed to fetch audio. Please try again.');
        }
    } catch (error) {
        console.error('Error fetching audio:', error);
        alert('An error occurred while fetching the audio.');
    }
});

// Add event listeners for custom controls
const audioPlayer = document.getElementById('audio-player');
document.getElementById('rewind-btn').addEventListener('click', () => {
    audioPlayer.currentTime -= 5; // Rewind 5 seconds
});
document.getElementById('fast-forward-btn').addEventListener('click', () => {
    audioPlayer.currentTime += 5; // Fast forward 5 seconds
});
document.getElementById('speed-control').addEventListener('change', (event) => {
    audioPlayer.playbackRate = parseFloat(event.target.value); // Adjust playback speed
});