/*
Author: Odon Mulambo
*/

document.addEventListener('DOMContentLoaded', () => {
    const sound = {
        'a': "http://carolinegabriel.com/demo/js-keyboard/sounds/040.wav",
        'w': "https://carolinegabriel.com/demo/js-keyboard/sounds/041.wav",
        's': "https://carolinegabriel.com/demo/js-keyboard/sounds/042.wav",
        'e': "https://carolinegabriel.com/demo/js-keyboard/sounds/043.wav",
        'd': "https://carolinegabriel.com/demo/js-keyboard/sounds/044.wav",
        'f': "https://carolinegabriel.com/demo/js-keyboard/sounds/045.wav",
        't': "https://carolinegabriel.com/demo/js-keyboard/sounds/046.wav",
        'g': "https://carolinegabriel.com/demo/js-keyboard/sounds/047.wav",
        'y': "https://carolinegabriel.com/demo/js-keyboard/sounds/048.wav",
        'h': "https://carolinegabriel.com/demo/js-keyboard/sounds/049.wav",
        'u': "https://carolinegabriel.com/demo/js-keyboard/sounds/050.wav",
        'j': "https://carolinegabriel.com/demo/js-keyboard/sounds/051.wav",
        'k': "https://carolinegabriel.com/demo/js-keyboard/sounds/052.wav",
        'o': "https://carolinegabriel.com/demo/js-keyboard/sounds/053.wav",
        'l': "https://carolinegabriel.com/demo/js-keyboard/sounds/054.wav",
        'p': "https://carolinegabriel.com/demo/js-keyboard/sounds/055.wav",
        ';': "https://carolinegabriel.com/demo/js-keyboard/sounds/056.wav"
    };
    let isAwakened = false;
    let audioEnabled = false;
    const sequence = [];
    const pianoContainer = document.querySelector('.piano-container');
    const MAX_SEQUENCE_LENGTH = 8; // "weseeyou".length

    // Enable audio after user interaction
    document.addEventListener('click', () => {
        audioEnabled = true;
        const testAudio = new Audio();
        testAudio.play().catch(err => console.error('Autoplay blocked:', err));
    });

    const keyMap = {
        'a': '#key-a', 's': '#key-s', 'd': '#key-d', 'f': '#key-f',
        'g': '#key-g', 'h': '#key-h', 'j': '#key-j', 'k': '#key-k',
        'l': '#key-l', ';': '#key-semicolon', 'w': '#key-w',
        'e': '#key-e', 't': '#key-t', 'y': '#key-y', 'u': '#key-u',
        'o': '#key-o', 'p': '#key-p'
    };

    // Function to handle key press or mouse click
    function playKey(key) {
        if (isAwakened || !audioEnabled) return;

        const element = document.querySelector(keyMap[key]);
        if (!element) {
            console.error(`No element found for key "${key}"`);
            return;
        }

        // Visual feedback
        element.classList.add('pressed');
        setTimeout(() => element.classList.remove('pressed'), 200);

        // Audio handling
        if (sound[key]) {
            const audio = new Audio(sound[key]);
            audio.play().catch(err => console.error(`Failed to play sound for key "${key}":`, err));
        }

        // Sequence detection
        sequence.push(key);
        if (sequence.length > MAX_SEQUENCE_LENGTH) sequence.shift();

        console.log('Current sequence:', sequence.join(''));

        if (sequence.join('') === 'weseeyou') {
            awakenOldOne();
        } else if (!'weseeyou'.startsWith(sequence.join(''))) {
            sequence.length = 0; // Reset if invalid sequence
        }
    }

    // Handle keyboard presses
    document.addEventListener('keydown', (e) => {
        const key = e.key.toLowerCase();
        playKey(key);
    });

    // Handle mouse clicks on piano keys
    document.querySelectorAll('.white-key, .black-key').forEach(keyElement => {
        keyElement.addEventListener('click', () => {
            const keyLabel = keyElement.querySelector('.key-label')?.textContent.trim().toLowerCase();
            if (keyLabel) {
                playKey(keyLabel);
            }
        });
    });

    async function awakenOldOne() {
        isAwakened = true;

        // Fade out piano
        pianoContainer.style.transition = 'opacity 1s';
        pianoContainer.style.opacity = '0';

        try {
            // Play creepy sound
            const creepyAudio = new Audio('https://orangefreesounds.com/wp-content/uploads/2020/09/Creepy-piano-sound-effect.mp3?_=1');
            await creepyAudio.play();
        } catch (err) {
            console.error('Creepy sound error:', err);
        }

        // Replace with image
        setTimeout(() => {
            pianoContainer.innerHTML = `
                <img src="../static/piano/images/texture.jpeg" 
                     alt="The Awakened Great Old One"
                     class="awakened-image">
            `;
            pianoContainer.style.opacity = '1';
        }, 1000);

        // Cleanup
        document.removeEventListener('keydown', handleKeyPress);
    }
});