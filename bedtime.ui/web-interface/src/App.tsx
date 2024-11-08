import { useState, useEffect, useRef } from 'react';
import { showToast, CustomToastContainer } from './components/CustomToast';
import DrawingCanvas, { DrawingCanvasHandle } from './components/DrawingCanvas';
import gura from './assets/gura.png';
import gura2 from './assets/gura2.png';
import AudioPlayer from './components/AudioPlayer';
import './App.css';

function App() {
  const [theme, setTheme] = useState<'mocha' | 'latte'>('mocha');
  const canvasRef = useRef<DrawingCanvasHandle>(null);
  const [isDownloadable, setIsDownloadable] = useState(false);

  const toggleTheme = () => {
    const newTheme = theme === 'mocha' ? 'latte' : 'mocha';
    setTheme(newTheme);
  };

  useEffect(() => {
    document.documentElement.classList.remove('mocha-theme', 'latte-theme');
    document.documentElement.classList.add(`${theme}-theme`);
  }, [theme]);

  const handleClearCanvas = () => {
    canvasRef.current?.clearCanvas();
    setIsDownloadable(false);
    showToast({ message: 'Canvas cleared!', theme });
  };

  const handleDownloadCanvas = () => {
    if (!isDownloadable) {
      showToast({ message: 'Please draw something first.', theme });
    } else {
      canvasRef.current?.downloadCanvas();
    }
  };

  useEffect(() => {
    const interval = setInterval(() => {
      if (canvasRef.current) {
        setIsDownloadable(canvasRef.current.hasDrawing());
      }
    }, 100);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="app">
      <header className="app-header">
        <div className="logo-container">
          <img
            src={gura}
            className="logo"
            alt="chibi"
            onClick={toggleTheme}
            style={{ cursor: 'pointer' }}
          />
        </div>
        <h1 className="app-title">Modern Deep Learning Interface</h1>
        <p className="app-description">
          Welcome to a sleek and modern interface for deep learning applications.
        </p>
      </header>

      <main className="main-content">
        <div className="card-container">
          <div className="card">
            <img src={gura2} alt="Card Image" className="card-image" />
            <div className="card-content">
              <h2>Gura</h2>
              <p>Train your models with cutting-edge algorithms and visualizations.</p>
            </div>
          </div>
        </div>

        <DrawingCanvas ref={canvasRef} />

        <div className="button-container">
          <button onClick={handleDownloadCanvas}>
            Download
          </button>
          <button onClick={handleClearCanvas}>Clear</button>
        </div>

        <div className="audio-player-section">
          <h2>Click Play</h2>
          <AudioPlayer theme={theme} />
        </div>
      </main>

      {/* Toast container */}
      <CustomToastContainer />

      <footer className="app-footer">
        <p>© 2024 Modern Deep Learning Interface</p>
      </footer>
    </div>
  );
}

export default App;
