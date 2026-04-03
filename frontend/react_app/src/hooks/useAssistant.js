import { useState } from 'react';
import { askAssistant } from '../services/apiClient';

export function useAssistant() {
  const [loading, setLoading] = useState(false);

  const submitQuestion = async (query) => {
    setLoading(true);
    try {
      const response = await askAssistant(query);
      return { answer: response.answer, sources: response.sources || [] };
    } catch {
      return { answer: 'Assistant is currently unavailable. Please try again later.', sources: [] };
    } finally {
      setLoading(false);
    }
  };

  return { loading, submitQuestion };
}
