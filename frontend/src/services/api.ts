const API_BASE_URL = 'http://localhost:8000/api';

export interface ChatResponse {
  success: boolean;
  response: string;
  timestamp: string;
}

export interface TTSResponse {
  success: boolean;
  audio_url?: string;
  filename?: string;
}

export interface ConversationHistory {
  total_messages: number;
  recent_messages: Array<{
    type: string;
    user_message?: string;
    response: string;
    timestamp: string;
  }>;
}

class ApiService {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  async sendTextMessage(message: string, userContext?: any): Promise<ChatResponse> {
    const response = await fetch(`${this.baseUrl}/chat/text`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
        user_context: userContext,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  async sendAudioMessage(audioFile: File): Promise<ChatResponse> {
    const formData = new FormData();
    formData.append('audio_file', audioFile);

    const response = await fetch(`${this.baseUrl}/chat/audio`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  async generateTTS(text: string, voice: string = 'nova', language: string = 'auto'): Promise<TTSResponse> {
    const response = await fetch(`${this.baseUrl}/tts/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text,
        voice,
        language,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  async streamTTS(text: string, voice: string = 'nova', language: string = 'auto'): Promise<Blob> {
    const response = await fetch(`${this.baseUrl}/tts/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text,
        voice,
        language,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.blob();
  }

  async getConversationHistory(): Promise<ConversationHistory> {
    const response = await fetch(`${this.baseUrl}/conversation/history`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data.data;
  }

  async clearConversation(): Promise<void> {
    const response = await fetch(`${this.baseUrl}/conversation/clear`, {
      method: 'POST',
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
  }

  async getStatus(): Promise<any> {
    const response = await fetch(`${this.baseUrl}/status`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  createWebSocket(clientId: string): WebSocket {
    const wsUrl = `ws://localhost:8000/api/ws/${clientId}`;
    return new WebSocket(wsUrl);
  }
}

export const apiService = new ApiService();
