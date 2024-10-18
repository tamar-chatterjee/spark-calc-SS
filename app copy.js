// Get references to HTML elements
const trackInputs = [document.getElementById('track1'), document.getElementById('track2')];
const switchButton = document.getElementById('switchButton');
const playButton = document.getElementById('playButton');
const stopButton = document.getElementById('stopButton');
const canvas = document.getElementById('visualizer');
const canvasCtx = canvas.getContext('2d');

canvas.width = canvas.offsetWidth;
canvas.height = canvas.offsetHeight;

// Audio context and variables
let audioCtx;
let analyser;
let dataArray;
let bufferLength;
let audioElements = [null, null];
let audioSources = [null, null];
let currentTrackIndex = 0;

// Add this variable to store the current playback time
let savedTime = 0;
let isVisualizing = false; // Flag to manage visualization state

// Initialize Audio Context on user interaction
function initAudioContext() {
    if (!audioCtx) {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }
}

// Handle file uploads
trackInputs.forEach((input, index) => {
    input.addEventListener('change', event => {
        const file = event.target.files[0];
        if (file) {
            const fileURL = URL.createObjectURL(file);
            loadTrack(fileURL, index);
        }
    });
});

// Load and play the audio track
function loadTrack(url, index) {
    initAudioContext();

    // Create audio element
    const audio = new Audio();
    audio.src = url;
    audio.crossOrigin = 'anonymous';
    audio.loop = true; // Optional: Loop the audio

    // Create media element source
    const source = audioCtx.createMediaElementSource(audio);

    // Create analyser if not exists
    if (!analyser) {
        analyser = audioCtx.createAnalyser();
        analyser.fftSize = 256;
        bufferLength = analyser.frequencyBinCount;
        dataArray = new Uint8Array(bufferLength);
    }

    // Connect nodes
    source.connect(analyser);
    analyser.connect(audioCtx.destination);

    // Store references
    audioElements[index] = audio;
    audioSources[index] = source;

    // Auto-play if it's the first track loaded
    if (index === currentTrackIndex) {
        playTrack(index);
    }
}

// Play the selected track
function playTrack(index) {
    // Pause the other track and save the current time
    const otherIndex = (index + 1) % 2;
    if (audioElements[otherIndex]) {
        savedTime = audioElements[otherIndex].currentTime;
        audioElements[otherIndex].pause();
    }

    // Ensure savedTime doesn't exceed the duration of the new track
    const audio = audioElements[index];
    if (audio) {
        // Wait until the audio metadata is loaded
        if (audio.readyState >= 1) {
            setCurrentTimeAndPlay(audio);
        } else {
            audio.addEventListener('loadedmetadata', () => {
                setCurrentTimeAndPlay(audio);
            });
        }
    }
}

function setCurrentTimeAndPlay(audio) {
    // Adjust savedTime if it exceeds the audio duration
    if (savedTime > audio.duration) {
        savedTime = audio.duration;
    }

    audio.currentTime = savedTime;
    audio.play();
    if (!isVisualizing) {
        isVisualizing = true;
        visualize();
    }
}

// Play and Stop functions
function playCurrentTrack() {
    const audio = audioElements[currentTrackIndex];
    if (audio) {
        audio.play();
        if (!isVisualizing) {
            isVisualizing = true;
            visualize();
        }
    }
}

function stopCurrentTrack() {
    const audio = audioElements[currentTrackIndex];
    if (audio) {
        audio.pause();
        audio.currentTime = 0;
        isVisualizing = false;
        clearCanvas();
    }
}

// Event listeners for Play and Stop buttons
playButton.addEventListener('click', playCurrentTrack);
stopButton.addEventListener('click', stopCurrentTrack);

// Switch between tracks
switchButton.addEventListener('click', () => {
    currentTrackIndex = (currentTrackIndex + 1) % 2;
    playTrack(currentTrackIndex);
});

// Visualization function
function visualize() {
    if (!isVisualizing) return;

    requestAnimationFrame(visualize);

    if (!analyser) return;

    analyser.getByteFrequencyData(dataArray);

    canvasCtx.fillStyle = '#000';
    canvasCtx.fillRect(0, 0, canvas.width, canvas.height);

    const barWidth = (canvas.width / bufferLength) * 2.5;
    let x = 0;

    for (let i = 0; i < bufferLength; i++) {
        const barHeight = dataArray[i];
        const r = barHeight + (25 * (i / bufferLength));
        const g = 250 * (i / bufferLength);
        const b = 50;

        canvasCtx.fillStyle = `rgb(${r},${g},${b})`;
        canvasCtx.fillRect(x, canvas.height - barHeight, barWidth, barHeight);

        x += barWidth + 1;
    }
}

// Function to clear the canvas
function clearCanvas() {
    canvasCtx.fillStyle = '#000';
    canvasCtx.fillRect(0, 0, canvas.width, canvas.height);
}
