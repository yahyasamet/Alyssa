/**
 * app.js: JS code for the adk-streaming sample app.
 */

// Import the audio worklets and blob visualizer first
import { startAudioPlayerWorklet } from "./audio-player.js";
import { startAudioRecorderWorklet } from "./audio-recorder.js";
import BlobVisualizer from "./blob-visualizer.js";

/**
 * WebSocket handling
 */

// Global variables
const sessionId = Math.random().toString().substring(10);
const ws_url = "ws://" + window.location.host + "/ws/" + sessionId;
let websocket = null;
let is_audio = false;
let currentMessageId = null; // Track the current message ID during a conversation turn

// Audio variables
let audioPlayerNode;
let audioPlayerContext;
let audioRecorderNode;
let audioRecorderContext;
let micStream;
let isRecording = false;
let blobVisualizer;
let speakingAnimation;

// Get DOM elements
const messageForm = document.getElementById("messageForm");
const messageInput = document.getElementById("message");
const messagesDiv = document.getElementById("messages");
const statusDot = document.getElementById("status-dot");
const connectionStatus = document.getElementById("connection-text");
const typingIndicator = document.getElementById("typing-indicator");
const startAudioButton = document.getElementById("startAudioButton");
const stopAudioButton = document.getElementById("stopAudioButton");
const recordingIndicator = document.getElementById("recording-indicator");
const voiceBlob = document.getElementById("voice-blob");
const stateText = document.getElementById("state-text");
const blobContainer = document.getElementById("blob-container");
const siriwaveContainer = document.getElementById("siriwave-container");
const siriMessage = document.getElementById("siri-message");

// SiriWave instance
let siriWave = null;

// Blob state management
class BlobStateManager {
  constructor() {
    this.currentState = 'idle';
    this.stateTexts = {
      idle: 'جاهز للمساعدة',
      listening: 'أستمع إليك...',
      speaking: 'أليسا تتحدث...',
      thinking: 'أفكر...'
    };
  }

  setState(newState) {
    if (this.currentState !== newState) {
      console.log(`Blob state changing from ${this.currentState} to ${newState}`);
      
      // Handle thinking and speaking states - show SiriWave, hide blob
      if (newState === 'speaking' || newState === 'thinking') {
        this.showSiriWave();
      } else {
        this.hideSiriWave();
      }
      
      // Remove all state classes
      voiceBlob.classList.remove('idle', 'listening', 'speaking', 'thinking');
      
      // Add new state class
      voiceBlob.classList.add(newState);
      
      // Update state text
      if (stateText) {
        stateText.textContent = this.stateTexts[newState] || this.stateTexts.idle;
      }
      
      // Update siri message for thinking and speaking
      if ((newState === 'speaking' || newState === 'thinking') && siriMessage) {
        siriMessage.textContent = this.stateTexts[newState];
      }
      
      // Update current state
      this.currentState = newState;
      
      console.log(`Blob state successfully changed to: ${newState}`);
    }
  }

  showSiriWave() {
    console.log('Attempting to show SiriWave...');
    if (blobContainer && siriwaveContainer) {
      console.log('Containers found, proceeding with SiriWave display');
      // Hide blob container
      blobContainer.classList.add('hidden');
      
      // Add state class to SiriWave container for CSS styling
      siriwaveContainer.classList.remove('thinking', 'speaking');
      siriwaveContainer.classList.add(this.currentState);
      
      // Show SiriWave container
      setTimeout(() => {
        siriwaveContainer.classList.add('visible');
        console.log('SiriWave container should now be visible');
      }, 50);
      
      // Initialize SiriWave if not already done
      this.initSiriWave();
      
      // Start SiriWave animation with different settings based on state
      if (siriWave) {
        // Adjust animation based on current state
        if (this.currentState === 'thinking') {
          siriWave.setAmplitude(0.5); // Lower amplitude for thinking
          siriWave.setSpeed(0.1); // Slower speed for thinking
        } else if (this.currentState === 'speaking') {
          siriWave.setAmplitude(1); // Higher amplitude for speaking
          siriWave.setSpeed(0.2); // Normal speed for speaking
        }
        siriWave.start();
        console.log('SiriWave animation started for state:', this.currentState);
      } else {
        console.log('Using fallback wave animation');
        // Fallback is already animated via CSS
      }
    } else {
      console.error('SiriWave containers not found:', {
        blobContainer: !!blobContainer,
        siriwaveContainer: !!siriwaveContainer
      });
    }
  }

  hideSiriWave() {
    if (blobContainer && siriwaveContainer) {
      // Hide SiriWave container
      siriwaveContainer.classList.remove('visible');
      
      // Show blob container
      blobContainer.classList.remove('hidden');
      
      // Stop SiriWave animation
      if (siriWave) {
        siriWave.stop();
      }
      
      console.log('SiriWave hidden, blob container shown');
    }
  }

  initSiriWave() {
    console.log('Initializing SiriWave...', {
      siriWaveExists: !!siriWave,
      SiriWaveClassExists: !!window.SiriWave
    });
    
    if (!siriWave && window.SiriWave) {
      try {
        // Calculate responsive dimensions
        const container = document.getElementById("siri-wave");
        if (!container) {
          console.error('SiriWave container element not found');
          this.createFallbackWave();
          return;
        }
        
        const maxWidth = Math.min(640, window.innerWidth - 40);
        const width = maxWidth;
        const height = Math.max(150, Math.min(200, width * 0.3125)); // Maintain aspect ratio
        
        console.log('Creating SiriWave with dimensions:', { width, height });
        
        siriWave = new SiriWave({
          container: container,
          width: width,
          height: height,
          style: "ios9",
          amplitude: 1,
          speed: 0.2,
          autostart: false,
          color: "#667eea",
          frequency: 6,
          globalCompositeOperation: 'lighter'
        });
        console.log('SiriWave initialized successfully');
      } catch (error) {
        console.error('Error initializing SiriWave:', error);
        this.createFallbackWave();
      }
    } else if (!window.SiriWave) {
      console.error('SiriWave library not loaded, using fallback');
      this.createFallbackWave();
    } else {
      console.log('SiriWave already initialized');
    }
  }

  createFallbackWave() {
    const container = document.getElementById("siri-wave");
    if (container && !container.querySelector('.siri-wave-fallback')) {
      container.innerHTML = `
        <div class="siri-wave-fallback">
          <div class="wave-bar"></div>
          <div class="wave-bar"></div>
          <div class="wave-bar"></div>
          <div class="wave-bar"></div>
          <div class="wave-bar"></div>
          <div class="wave-bar"></div>
          <div class="wave-bar"></div>
          <div class="wave-bar"></div>
          <div class="wave-bar"></div>
          <div class="wave-bar"></div>
          <div class="wave-bar"></div>
        </div>
      `;
      console.log('Fallback wave animation created');
    }
  }

  getState() {
    return this.currentState;
  }
}

// Initialize blob state manager
const blobState = new BlobStateManager();

// DOM Content Loaded Event
document.addEventListener('DOMContentLoaded', function() {
  console.log('DOM loaded, initializing blob visualizer...');
  
  // Check if all elements exist
  if (!voiceBlob) {
    console.error('Voice blob element not found!');
    return;
  }
  if (!stateText) {
    console.error('State text element not found!');
    return;
  }
  
  // Initialize blob visualizer
  try {
    blobVisualizer = new BlobVisualizer(voiceBlob);
    console.log('Blob visualizer initialized successfully');
  } catch (error) {
    console.error('Error initializing blob visualizer:', error);
  }
  
  // Initialize connection status
  statusDot.classList.add("connecting");
  connectionStatus.textContent = "جاري الاتصال...";
  blobState.setState('idle');
  
  // Wait for SiriWave library to load and then initialize Textillate
  setTimeout(() => {
    console.log('Checking for SiriWave availability:', !!window.SiriWave);
    
    // Initialize Textillate when jQuery is available
    if (window.$ && $.fn.textillate) {
      $('.siri-message').textillate({
        loop: false,
        sync: true,
        in: {
          effect: "fadeInUp",
          sync: true,
          delay: 50
        },
        out: {
          effect: "fadeOutUp",
          sync: true,
          delay: 50
        },
      });
      console.log('Textillate initialized successfully');
    } else {
      console.warn('jQuery or Textillate not available');
    }
  }, 500); // Give time for all external libraries to load
});

// Add blob click interaction
voiceBlob.addEventListener('click', () => {
  if (!is_audio && websocket && websocket.readyState === WebSocket.OPEN) {
    // If voice is not enabled, enable it
    startAudioButton.click();
  } else if (is_audio) {
    // If voice is enabled, toggle recording state
    // This provides visual feedback when user interacts with blob
    if (blobState.getState() === 'listening') {
      blobState.setState('idle');
      setTimeout(() => blobState.setState('listening'), 500);
    }
  }
});

// Add hover effects for blob
voiceBlob.addEventListener('mouseenter', () => {
  if (blobState.getState() === 'idle') {
    voiceBlob.style.transform = 'scale(1.05)';
  }
});

voiceBlob.addEventListener('mouseleave', () => {
  voiceBlob.style.transform = 'scale(1)';
});

// WebSocket handlers
function connectWebsocket() {
  // Connect websocket
  const wsUrl = ws_url + "?is_audio=" + is_audio;
  websocket = new WebSocket(wsUrl);

  // Handle connection open
  websocket.onopen = function () {
    // Connection opened messages
    console.log("WebSocket connection opened.");
    connectionStatus.textContent = "متصل";
    statusDot.classList.remove("connecting");
    statusDot.classList.add("connected");

    // Set blob to idle state
    blobState.setState('idle');

    // Enable the Send button
    document.getElementById("sendButton").disabled = false;
    addSubmitHandler();
  };

  // Handle incoming messages
  websocket.onmessage = function (event) {
    // Parse the incoming message
    const message_from_server = JSON.parse(event.data);
    console.log("[AGENT TO CLIENT] ", message_from_server);

    // Show typing indicator for first message in a response sequence,
    // but not for turn_complete messages
    if (
      !message_from_server.turn_complete &&
      (message_from_server.mime_type === "text/plain" ||
        message_from_server.mime_type === "audio/pcm")
    ) {
      typingIndicator.classList.add("visible");
      blobState.setState('thinking');
    }

    // Check if the turn is complete
    if (
      message_from_server.turn_complete &&
      message_from_server.turn_complete === true
    ) {
      // Reset currentMessageId to ensure the next message gets a new element
      currentMessageId = null;
      typingIndicator.classList.remove("visible");
      
      // Return blob to idle state when turn is complete
      if (speakingAnimation) {
        speakingAnimation.cancel();
        speakingAnimation = null;
      }
      
      // Stop SiriWave and show blob again
      blobState.setState('idle');
      return;
    }

    // If it's audio, play it
    if (message_from_server.mime_type === "audio/pcm" && audioPlayerNode) {
      console.log('Audio message received, setting speaking state');
      audioPlayerNode.port.postMessage(base64ToArray(message_from_server.data));
      
      // Hide typing indicator when speaking starts
      typingIndicator.classList.remove("visible");
      
      // Set blob to speaking state during audio playback
      blobState.setState('speaking');
      
      // Start speaking animation
      if (speakingAnimation) {
        speakingAnimation.cancel();
      }
      if (blobVisualizer) {
        speakingAnimation = blobVisualizer.createSpeakingAnimation();
      }

      // If we have an existing message element for this turn, add audio icon if needed
      if (currentMessageId) {
        const messageElem = document.getElementById(currentMessageId);
        if (
          messageElem &&
          !messageElem.querySelector(".audio-icon") &&
          is_audio
        ) {
          const audioIcon = document.createElement("span");
          audioIcon.className = "audio-icon";
          messageElem.prepend(audioIcon);
        }
      }
    }

    // Handle text messages
    if (message_from_server.mime_type === "text/plain") {
      // Hide typing indicator
      typingIndicator.classList.remove("visible");

      const role = message_from_server.role || "model";

      // If we already have a message element for this turn, append to it
      if (currentMessageId && role === "model") {
        const existingMessage = document.getElementById(currentMessageId);
        if (existingMessage) {
          // Append the text without adding extra spaces
          // Use a span element to maintain proper text flow
          const textNode = document.createTextNode(message_from_server.data);
          existingMessage.appendChild(textNode);

          // Scroll to the bottom
          messagesDiv.scrollTop = messagesDiv.scrollHeight;
          return;
        }
      }

      // Create a new message element if it's a new turn or user message
      const messageId = Math.random().toString(36).substring(7);
      const messageElem = document.createElement("p");
      messageElem.id = messageId;

      // Set class based on role
      messageElem.className =
        role === "user" ? "user-message" : "agent-message";

      // Add audio icon for model messages if audio is enabled
      if (is_audio && role === "model") {
        const audioIcon = document.createElement("span");
        audioIcon.className = "audio-icon";
        messageElem.appendChild(audioIcon);
      }

      // Add the text content
      messageElem.appendChild(
        document.createTextNode(message_from_server.data)
      );

      // Add the message to the DOM
      messagesDiv.appendChild(messageElem);

      // Remember the ID of this message for subsequent responses in this turn
      if (role === "model") {
        currentMessageId = messageId;
      }

      // Scroll to the bottom
      messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }
  };

  // Handle connection close
  websocket.onclose = function () {
    console.log("WebSocket connection closed.");
    document.getElementById("sendButton").disabled = true;
    connectionStatus.textContent = "منقطع. جاري إعادة الاتصال...";
    statusDot.classList.remove("connected");
    statusDot.classList.add("connecting");
    typingIndicator.classList.remove("visible");
    
    // Set blob to idle state on disconnect
    blobState.setState('idle');
    
    setTimeout(function () {
      console.log("Reconnecting...");
      connectWebsocket();
    }, 5000);
  };

  websocket.onerror = function (e) {
    console.log("WebSocket error: ", e);
    connectionStatus.textContent = "خطأ في الاتصال";
    statusDot.classList.remove("connected");
    statusDot.classList.add("disconnected");
    typingIndicator.classList.remove("visible");
    
    // Set blob to idle state on error
    blobState.setState('idle');
  };
}
connectWebsocket();

// Add submit handler to the form
function addSubmitHandler() {
  messageForm.onsubmit = function (e) {
    e.preventDefault();
    const message = messageInput.value;
    if (message) {
      const p = document.createElement("p");
      p.textContent = message;
      p.className = "user-message";
      messagesDiv.appendChild(p);
      messageInput.value = "";

      // Show typing indicator after sending message
      typingIndicator.classList.add("visible");

      sendMessage({
        mime_type: "text/plain",
        data: message,
        role: "user",
      });
      console.log("[CLIENT TO AGENT] " + message);
      // Scroll down to the bottom of the messagesDiv
      messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }
    return false;
  };
}

// Send a message to the server as a JSON string
function sendMessage(message) {
  if (websocket && websocket.readyState == WebSocket.OPEN) {
    const messageJson = JSON.stringify(message);
    websocket.send(messageJson);
  }
}

// Decode Base64 data to Array
function base64ToArray(base64) {
  const binaryString = window.atob(base64);
  const len = binaryString.length;
  const bytes = new Uint8Array(len);
  for (let i = 0; i < len; i++) {
    bytes[i] = binaryString.charCodeAt(i);
  }
  return bytes.buffer;
}

/**
 * Audio handling
 */

// Start audio
function startAudio() {
  // Start audio output
  startAudioPlayerWorklet().then(([node, ctx]) => {
    audioPlayerNode = node;
    audioPlayerContext = ctx;
  });
  // Start audio input
  startAudioRecorderWorklet(audioRecorderHandler).then(
    ([node, ctx, stream]) => {
      audioRecorderNode = node;
      audioRecorderContext = ctx;
      micStream = stream;
      isRecording = true;
      
      // Set blob to listening state when recording starts
      blobState.setState('listening');
    }
  );
}

// Stop audio recording
function stopAudio() {
  if (audioRecorderNode) {
    audioRecorderNode.disconnect();
    audioRecorderNode = null;
  }

  if (audioRecorderContext) {
    audioRecorderContext
      .close()
      .catch((err) => console.error("Error closing audio context:", err));
    audioRecorderContext = null;
  }

  if (micStream) {
    micStream.getTracks().forEach((track) => track.stop());
    micStream = null;
  }

  isRecording = false;
  
  // Stop blob visualizations
  if (blobVisualizer) {
    blobVisualizer.stopAllAnimations();
  }
  
  // Set blob back to idle state
  blobState.setState('idle');
}

// Start the audio only when the user clicked the button
// (due to the gesture requirement for the Web Audio API)
startAudioButton.addEventListener("click", () => {
  startAudioButton.disabled = true;
  startAudioButton.innerHTML = `
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
      <path d="M12 1C10.34 1 9 2.34 9 4V12C9 13.66 10.34 15 12 15C13.66 15 15 13.66 15 12V4C15 2.34 13.66 1 12 1ZM19 10V12C19 16.42 15.42 20 11 20V22H13V24H11H9V22H11V20C6.58 20 3 16.42 3 12V10H5V12C5 15.31 7.69 18 11 18V16C11 15.45 11.45 15 12 15C12.55 15 13 15.45 13 16V18C16.31 18 19 15.31 19 12V10Z" fill="currentColor"/>
    </svg>
    <span>Voice Enabled</span>
  `;
  startAudioButton.style.display = "none";
  stopAudioButton.style.display = "inline-flex";
  recordingIndicator.style.display = "flex";
  
  // Set blob to listening state
  blobState.setState('listening');
  
  startAudio();
  is_audio = true;

  // Add class to messages container to enable audio styling
  messagesDiv.classList.add("audio-enabled");

  connectWebsocket(); // reconnect with the audio mode
});

// Stop audio recording when stop button is clicked
stopAudioButton.addEventListener("click", () => {
  stopAudio();
  stopAudioButton.style.display = "none";
  startAudioButton.style.display = "inline-flex";
  startAudioButton.disabled = false;
  startAudioButton.innerHTML = `
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
      <path d="M12 1C10.34 1 9 2.34 9 4V12C9 13.66 10.34 15 12 15C13.66 15 15 13.66 15 12V4C15 2.34 13.66 1 12 1ZM19 10V12C19 16.42 15.42 20 11 20V22H13V24H11H9V22H11V20C6.58 20 3 16.42 3 12V10H5V12C5 15.31 7.69 18 11 18V16C11 15.45 11.45 15 12 15C12.55 15 13 15.45 13 16V18C16.31 18 19 15.31 19 12V10Z" fill="currentColor"/>
    </svg>
    <span>Enable Voice</span>
  `;
  recordingIndicator.style.display = "none";

  // Remove audio styling class
  messagesDiv.classList.remove("audio-enabled");
  
  // Set blob back to idle state
  blobState.setState('idle');

  // Reconnect without audio mode
  is_audio = false;

  // Only reconnect if the connection is still open
  if (websocket && websocket.readyState === WebSocket.OPEN) {
    websocket.close();
    // The onclose handler will trigger reconnection
  }
});

// Audio recorder handler
function audioRecorderHandler(pcmData) {
  // Only send data if we're still recording
  if (!isRecording) return;

  // Calculate audio level for visual feedback
  const audioArray = new Float32Array(pcmData);
  let sum = 0;
  for (let i = 0; i < audioArray.length; i++) {
    sum += Math.abs(audioArray[i]);
  }
  const audioLevel = sum / audioArray.length;
  
  // Update blob visualization based on audio level
  if (blobVisualizer && audioLevel > 0.01) {
    blobVisualizer.updateBlobVisualization(audioLevel * 10); // Scale for better visibility
  }

  // Send the pcm data as base64
  sendMessage({
    mime_type: "audio/pcm",
    data: arrayBufferToBase64(pcmData),
  });

  // Log every few samples to avoid flooding the console
  if (Math.random() < 0.01) {
    // Only log ~1% of audio chunks
    console.log("[CLIENT TO AGENT] sent audio data", `Level: ${audioLevel.toFixed(4)}`);
  }
}

// Encode an array buffer with Base64
function arrayBufferToBase64(buffer) {
  let binary = "";
  const bytes = new Uint8Array(buffer);
  const len = bytes.byteLength;
  for (let i = 0; i < len; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  return window.btoa(binary);
}

// Window resize handler for SiriWave
window.addEventListener('resize', () => {
  if (siriWave && blobState.getState() === 'speaking') {
    // Reinitialize SiriWave with new dimensions
    siriWave = null;
    blobState.initSiriWave();
  }
});

// Debug functions (remove in production)
window.testSpeakingState = function() {
  console.log('Testing speaking state...');
  if (blobState) {
    blobState.setState('speaking');
  }
};

window.testThinkingState = function() {
  console.log('Testing thinking state...');
  if (blobState) {
    blobState.setState('thinking');
  }
};

window.testIdleState = function() {
  console.log('Testing idle state...');
  if (blobState) {
    blobState.setState('idle');
  }
};

// Log current state
window.getCurrentState = function() {
  console.log('Current state:', blobState ? blobState.getState() : 'No state manager');
  console.log('SiriWave exists:', !!siriWave);
  console.log('SiriWave library loaded:', !!window.SiriWave);
};

// Initialize blob state manager
