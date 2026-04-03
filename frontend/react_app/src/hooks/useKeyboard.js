import { useEffect } from 'react';
import { useApp } from '../context/AppContext';

export default function useKeyboard() {
  const { openCommandPalette, closeCommandPalette, commandPaletteOpen } = useApp();

  useEffect(() => {
    function handleKeyDown(e) {
      // Cmd/Ctrl + K → open command palette
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        if (commandPaletteOpen) {
          closeCommandPalette();
        } else {
          openCommandPalette();
        }
      }
      // Escape → close command palette
      if (e.key === 'Escape' && commandPaletteOpen) {
        closeCommandPalette();
      }
    }

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [commandPaletteOpen, openCommandPalette, closeCommandPalette]);
}
