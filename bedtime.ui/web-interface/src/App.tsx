import { useState, useEffect, useRef } from 'react';
import { useSpring, animated } from '@react-spring/web';
import { showToast, CustomToastContainer } from './components/CustomToast';
import DrawingCanvas, { DrawingCanvasHandle } from './components/DrawingCanvas';
import gura from './assets/gura.png';
import AudioPlayer from './components/AudioPlayer';
import './App.css';

function importAllImages() {
  const images = import.meta.glob('./assets/demo*.png', { eager: true });
  return Object.values(images).map((module: any) => module.default);
}

function App() {
  const [theme, setTheme] = useState<'mocha' | 'latte'>('mocha');
  const canvasRef = useRef<DrawingCanvasHandle>(null);
  const [isDownloadable, setIsDownloadable] = useState(false);
  const [demoImages, setDemoImages] = useState<string[]>([]);

  const toggleTheme = () => {
    const newTheme = theme === 'mocha' ? 'latte' : 'mocha';
    setTheme(newTheme);
  };

  // Load images and apply theme on mount and theme change
  useEffect(() => {
    const images = importAllImages();
    setDemoImages(images);

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

  // Check if there's a drawing on the canvas at intervals
  useEffect(() => {
    const interval = setInterval(() => {
      if (canvasRef.current) {
        setIsDownloadable(canvasRef.current.hasDrawing());
      }
    }, 100);
    return () => clearInterval(interval);
  }, []);

  // Submit function to capture canvas data and make API call
  const handleSubmit = async () => {
    const canvasData = canvasRef.current?.getBase64FromCanvas();
  
    if (canvasData) {
      // Log the base64 data to verify it's correct
      console.log("Canvas Data:", canvasData);
  
      try {
        const response = await fetch('/infer/sketchclassify', { // Use relative path          
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            image_base64: canvasData
          }),
        });
  
        if (response.ok) {
          const result = await response.json();
          showToast({ 
            message: `\n Thats an amazing ${result.prediction}, I'm  ${result.confidence * 100}% confident`, 
            theme 
          });
                  } else {
          // Log additional error details for clarity
          console.error("Submission failed:", response.status, response.statusText);
          showToast({ message: `Submission failed with status ${response.status}.`, theme });
        }
      } catch (error) {
        console.error('Error submitting data:', error);
        showToast({ message: 'Network error.', theme });
      }
    } else {
      console.warn("No canvas data available.");
      showToast({ message: 'Canvas is empty.', theme });
    }
  };
  

  // Floating animation with react-spring
  const floatingAnimation = useSpring({
    from: { transform: 'translateY(0px) scale(1)' },
    to: async (next) => {
      while (true) {
        await next({ transform: 'translateY(-20px) scale(1.05)' });
        await next({ transform: 'translateY(20px) scale(0.95)' });
      }
    },
    config: { duration: 4000 },
  });

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
        <h1 className="app-title">bedtime.ai</h1>
        <p className="app-description">
          Your wildest imagination turned into intriguing stories!
        </p>
      </header>

      <main className="main-content">
        {/* Floating animated demo images */}
        <div className="floating-bubbles">
          {demoImages.map((image, index) => (
            <animated.div
              key={index}
              className="bubble"
              style={{
                ...floatingAnimation,
                backgroundImage: `url(${image})`,
              }}
            />
          ))}
        </div>

        <DrawingCanvas ref={canvasRef} />

        <div className="button-container">
          <button onClick={handleDownloadCanvas}>Download</button>
          <button onClick={handleClearCanvas}>Clear</button>
          <button onClick={handleSubmit}>Submit</button> {/* Submit Button */}
        </div>

        <div className="audio-player-section">
          <h2>Click Play</h2>
          <AudioPlayer theme={theme} />
        </div>
      </main>

      <CustomToastContainer />

      <footer className="app-footer">
        <p>Made with ❤️ with React and Catppuccin</p>
        <p>© 2024 bedtime.ai</p>
      </footer>
    </div>
  );
}

export default App;
