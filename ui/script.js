const container = document.querySelector('.orb-container');
    const orb = container.querySelector('.orb');
    const eyesContainer = document.querySelector('.eyes');
    const eyes = document.querySelectorAll('.eye');
    const flash = document.querySelector('.flash');
    let state = "idle";

    // Random eye movement
    function randomEyeMovement() {
      if (state !== "camera") {
        const moveX = (Math.random() - 0.5) * 25;
        const moveY = (Math.random() - 0.5) * 15;
        eyes.forEach(eye => eye.style.transform = `translate(${moveX}px, ${moveY}px)`);
      }
      setTimeout(randomEyeMovement, 800 + Math.random() * 2500);
    }
    randomEyeMovement();

    // Eye blink animation
    setInterval(() => {
      if (state !== "camera" && Math.random() > 0.65) {
        eyes.forEach(eye => {
          eye.style.height = '6px';
          setTimeout(() => eye.style.height = '80px', 180);
        });
      }
    }, 2800);

    // Change orb color
    function changeColor(color) {
        container.className = `orb-container color-${color}`;
        const pixelatedBg = container.querySelector('.pixelated-bg');

        // Fade out slightly for smooth cross-transition
        pixelatedBg.style.opacity = 0.6;

        // Delay gradient update slightly to sync with orb
        setTimeout(() => {
            if (color === 'blue') {
            pixelatedBg.style.background = `
                radial-gradient(ellipse 120% 100% at 50% 50%,
                rgba(100, 150, 255, 0.8) 0%,
                rgba(150, 100, 255, 0.6) 40%,
                rgba(100, 200, 200, 0.4) 70%,
                transparent 100%)`;
            } else if (color === 'orange') {
            pixelatedBg.style.background = `
                radial-gradient(ellipse 120% 100% at 50% 50%,
                rgba(255, 180, 100, 0.8) 0%,
                rgba(255, 100, 50, 0.6) 40%,
                rgba(255, 200, 100, 0.4) 70%,
                transparent 100%)`;
            } else if (color === 'green') {
            pixelatedBg.style.background = `
                radial-gradient(ellipse 120% 100% at 50% 50%,
                rgba(100, 255, 150, 0.8) 0%,
                rgba(150, 255, 100, 0.6) 40%,
                rgba(100, 200, 255, 0.4) 70%,
                transparent 100%)`;
            }

            // Fade back in
            pixelatedBg.style.opacity = 1;
        }, 100);
    }


    // Switch states
    function switchState(newState) {
      if (state === newState) return;
      state = newState;
      console.log(`Switching to ${state}`);

      const orb = document.querySelector('.orb');
      const container = document.querySelector('.orb-container');
      const recOverlay = document.querySelector('.recording-overlay');
      const feed = document.getElementById('camera-feed');

      // Reset classes
      orb.classList.remove('pulsing');
      container.classList.remove('recording');
      recOverlay?.classList.remove('visible');

      // --- State handling ---
      if (state === "thinking") {
        changeColor("orange");
      }
      else if (state === "answering") {
        changeColor("green");
        setTimeout(() => orb.classList.add("pulsing"), 350);
      }
      else if (state === "camera") {
        changeColor("blue");
        container.classList.add("camera");
      }
      else if (state === "recording") {
        container.classList.add("recording");
        recOverlay?.classList.add("visible");
      }
      else {
        // default: idle
        changeColor("blue");
      }
    }


    const spotifyInfo = document.getElementById("spotify-info");
    const currentTimeEl = document.getElementById("current-time");
    const statusBar = document.getElementById("status-bar");

    // Update clock every second
    setInterval(() => {
      const now = new Date();
      const timeStr = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      currentTimeEl.textContent = `${timeStr}`;
    }, 1000);

    // Update Spotify info from backend (via webview or websocket)
    window.updateSpotify = function(song, artist, isPlaying = true) {
      if (isPlaying) {
        spotifyInfo.textContent = `${song} — ${artist}`;
        statusBar.classList.add("playing");
      } else {
        spotifyInfo.textContent = "🎵 Not playing";
        statusBar.classList.remove("playing");
      }
    };