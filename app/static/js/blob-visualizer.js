/**
 * Advanced Blob Visualizer
 * Provides audio-reactive animations for the voice blob
 */

export class BlobVisualizer {
  constructor(blobElement) {
    this.blob = blobElement;
    this.blobCore = blobElement.querySelector('.blob-core');
    this.particles = blobElement.querySelectorAll('.particle');
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
  }
  // Update blob visualization based on audio data
  updateBlobVisualization(volume) {
    if (!this.blobCore) {
      console.warn('Blob core element not found');
      return;
    }

    try {
      // Scale blob based on volume
      const scale = 1 + Math.min(volume * 0.3, 0.5); // Cap the scaling
      const blur = Math.max(0, Math.min(volume * 3, 5)); // Cap the blur
      
      // Apply transforms
      this.blobCore.style.transform = `scale(${scale})`;
      this.blobCore.style.filter = `blur(${blur}px)`;

      // Animate particles based on volume
      this.particles.forEach((particle, index) => {
        if (particle) {
          const delay = index * 100;
          const intensity = Math.min(volume * (0.5 + Math.random() * 0.5), 1);
          
          particle.style.opacity = intensity;
          particle.style.transform = `scale(${1 + intensity})`;
        }
      });
    } catch (error) {
      console.error('Error updating blob visualization:', error);
    }
  }

  // Create pulsing effect for different states
  createPulseEffect(intensity = 1, duration = 2000) {
    if (!this.blobCore) return;

    const pulseAnimation = this.blobCore.animate([
      { transform: 'scale(1)', filter: 'blur(1px)' },
      { transform: `scale(${1 + intensity * 0.2})`, filter: `blur(${intensity * 2}px)` },
      { transform: 'scale(1)', filter: 'blur(1px)' }
    ], {
      duration: duration,
      easing: 'ease-in-out',
      iterations: 1
    });

    return pulseAnimation;
  }
  // Create speaking animation without audio analysis
  createSpeakingAnimation() {
    if (!this.blobCore) {
      console.warn('Blob core element not found for speaking animation');
      return null;
    }

    try {
      const speakingAnimation = this.blobCore.animate([
        { transform: 'scale(1)', borderRadius: '50% 50% 50% 50% / 50% 50% 50% 50%' },
        { transform: 'scale(1.1)', borderRadius: '70% 30% 30% 70% / 60% 40% 60% 40%' },
        { transform: 'scale(0.95)', borderRadius: '30% 70% 70% 30% / 40% 60% 40% 60%' },
        { transform: 'scale(1.05)', borderRadius: '60% 40% 40% 60% / 70% 30% 70% 30%' },
        { transform: 'scale(1)', borderRadius: '50% 50% 50% 50% / 50% 50% 50% 50%' }
      ], {
        duration: 1500,
        easing: 'ease-in-out',
        iterations: Infinity
      });

      return speakingAnimation;
    } catch (error) {
      console.error('Error creating speaking animation:', error);
      return null;
    }
  }

  // Stop all animations
  stopAllAnimations() {
    if (this.blobCore) {
      this.blobCore.getAnimations().forEach(animation => animation.cancel());
      this.blobCore.style.transform = '';
      this.blobCore.style.filter = '';
    }

    this.particles.forEach(particle => {
      particle.getAnimations().forEach(animation => animation.cancel());
      particle.style.opacity = '';
      particle.style.transform = '';
    });
  }
}

// Export for use in main app
export default BlobVisualizer;
