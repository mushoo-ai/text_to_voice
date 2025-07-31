
    const form = document.getElementById('voiceForm');
    const player = document.getElementById('player');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = new FormData(form);
        const response = await fetch('/speak', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const audioURL = '/audio?' + new Date().getTime(); // cache buster
            player.src = audioURL;
            player.style.display = 'block';

            // Wait until audio is ready before playing
            player.oncanplaythrough = () => {
                console.log("Audio ready, playing...");
                player.play().catch(err => {
                    console.error("Auto-play was blocked:", err);
                    alert("Click the play button to hear the audio.");
                });
            };
        } else {
            alert("Failed to generate audio.");
        }
    });
