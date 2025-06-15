/**
 * Advanced Blob Visualizer
 * Provides audio-reactive animations for the voice blob
 */

export class BlobVisualizer {
  constructor(blobElement) {
    this.blob = blobElement;
    this.ovalSpans = blobElement.querySelectorAll('.square span');
    this.isVisualizingAudio = false;
    this.animationFrame = null;
    this.audioData = new Float32Array(256);
    this.smoothedData = new Float32Array(256);
  }

  // Start audio visualization
  startAudioVisualization(audioContext, sourceNode) {
    if (!audioContext || !sourceNode) return;

    this.analyser = audioContext.createAnalyser();
    this.analyser.fftSize = 512;
    this.analyser.smoothingTimeConstant = 0.8;
    
    sourceNode.connect(this.analyser);
    this.isVisualizingAudio = true;
    this.visualizeAudio();
  }

  // Stop audio visualization
  stopAudioVisualization() {
    this.isVisualizingAudio = false;
    if (this.animationFrame) {
      cancelAnimationFrame(this.animationFrame);
    }
    if (this.analyser) {
      this.analyser.disconnect();
    }
  }

  // Main visualization loop
  visualizeAudio() {
    if (!this.isVisualizingAudio) return;

    this.analyser.getFloatFrequencyData(this.audioData);
    
    // Smooth the data
    for (let i = 0; i < this.audioData.length; i++) {
      this.smoothedData[i] = this.smoothedData[i] * 0.8 + this.audioData[i] * 0.2;
    }

    // Calculate average volume
    const avgVolume = this.smoothedData.reduce((sum, val) => sum + Math.abs(val), 0) / this.smoothedData.length;
    const normalizedVolume = Math.max(0, (avgVolume + 140) / 140); // Normalize -140dB to 0dB range

    // Update blob based on audio
    this.updateBlobVisualization(normalizedVolume);

    this.animationFrame = requestAnimationFrame(() => this.visualizeAudio());
  }  // Update blob visualization based on audio data
  updateBlobVisualization(volume) {
    if (!this.ovalSpans || this.ovalSpans.length === 0) {
      console.warn('Oval span elements not found');
      return;
    }

    try {
      // Scale and modify each oval span based on volume
      const baseIntensity = Math.min(volume * 2, 1);
      
      this.ovalSpans.forEach((span, index) => {
        if (span) {
          // Create varying intensities for each oval
          const intensity = baseIntensity * (0.7 + Math.random() * 0.6);
          const glowSize = 50 + (intensity * 30);
          
          // Update glow intensity based on audio
          span.style.filter = `blur(${Math.min(intensity * 3, 6)}px)`;
          
          // Modify box-shadow for audio reactivity
          const currentStyle = window.getComputedStyle(span);
          const currentColor = currentStyle.boxShadow.match(/rgb\([^)]+\)/)?.[0] || 'rgb(102, 126, 234)';
          
          span.style.boxShadow = `0 0 ${glowSize}px ${currentColor}, inset 0 0 ${glowSize}px ${currentColor}`;
        }
      });
    } catch (error) {
      console.error('Error updating oval visualization:', error);
    }
  }
  // Create pulsing effect for different states
  createPulseEffect(intensity = 1, duration = 2000) {
    if (!this.ovalSpans || this.ovalSpans.length === 0) return;

    const pulseAnimations = [];

    this.ovalSpans.forEach((span, index) => {
      if (span) {
        const delay = index * 200; // Stagger the animations
        const pulseAnimation = span.animate([
          { transform: 'rotate(0deg) scale(1)', filter: 'blur(0px)' },
          { transform: `rotate(${intensity * 45}deg) scale(${1 + intensity * 0.1})`, filter: `blur(${intensity}px)` },
          { transform: 'rotate(0deg) scale(1)', filter: 'blur(0px)' }
        ], {
          duration: duration,
          easing: 'ease-in-out',
          iterations: 1,
          delay: delay
        });

        pulseAnimations.push(pulseAnimation);
      }
    });

    return pulseAnimations;
  }  // Create speaking animation without audio analysis
  createSpeakingAnimation() {
    if (!this.ovalSpans || this.ovalSpans.length === 0) {
      console.warn('Oval span elements not found for speaking animation');
      return null;
    }

    try {
      const speakingAnimations = [];

      this.ovalSpans.forEach((span, index) => {
        if (span) {
          // Create different animation speeds for each oval
          const duration = 1000 + (index * 300); // Different durations
          
          const speakingAnimation = span.animate([
            { 
              borderRadius: '38% 62% 63% 37% / 41% 44% 56% 59%',
              transform: 'rotate(0deg)'
            },
            { 
              borderRadius: '70% 30% 30% 70% / 60% 40% 60% 40%',
              transform: 'rotate(120deg)'
            },
            { 
              borderRadius: '30% 70% 70% 30% / 40% 60% 40% 60%',
              transform: 'rotate(240deg)'
            },
            { 
              borderRadius: '38% 62% 63% 37% / 41% 44% 56% 59%',
              transform: 'rotate(360deg)'
            }
          ], {
            duration: duration,
            easing: 'ease-in-out',
            iterations: Infinity
          });

          speakingAnimations.push(speakingAnimation);
        }
      });

      return speakingAnimations;
    } catch (error) {
      console.error('Error creating speaking animation:', error);
      return null;
    }
  }
  // Stop all animations
  stopAllAnimations() {
    if (this.ovalSpans) {
      this.ovalSpans.forEach(span => {
        if (span) {
          span.getAnimations().forEach(animation => animation.cancel());
          span.style.transform = '';
          span.style.filter = '';
          span.style.boxShadow = '';
        }
      });
    }
  }
}

// Export for use in main app
export default BlobVisualizer;
