import React, { useState, useEffect, useRef } from 'react';
import { useSpring, animated } from '@react-spring/web';
import { showToast, CustomToastContainer } from './components/CustomToast';
import DrawingCanvas, { DrawingCanvasHandle } from './components/DrawingCanvas';
import gura from './assets/gura.png';
import AudioPlayer from './components/AudioPlayer';
import './App.css';

// Define the type for imported images
type ImageModule = {
  default: string;
};

// Function to import all images matching the pattern
function importAllImages(): string[] {
  const images: Record<string, ImageModule> = import.meta.glob('./assets/demo*.png', { eager: true });
  return Object.values(images).map((module) => module.default);
}

const App: React.FC = () => {
  const [theme, setTheme] = useState<'mocha' | 'latte'>('mocha');
  const canvasRef = useRef<DrawingCanvasHandle>(null);
  const [isDownloadable, setIsDownloadable] = useState(false);
  const [demoImages, setDemoImages] = useState<string[]>([]);
  const [audioData, setAudioData] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [messageIndex, setMessageIndex] = useState(0);
  const [progress, setProgress] = useState(0);

  const messages: string[] = [
    "Whoa! This drawing is so awesome—it needs a story!",
    "Let me think of something super fun to match it...",
    "Sprinkling a little magic dust... poof!",
    "Hang on, the adventure is coming together...",
    "Just a sec, your super cool story is almost done!",
  ];

  // Toggle between 'mocha' and 'latte' themes
  const toggleTheme = () => {
    const newTheme: 'mocha' | 'latte' = theme === 'mocha' ? 'latte' : 'mocha';
    setTheme(newTheme);
  };

  // Load demo images and apply theme classes
  useEffect(() => {
    const images = importAllImages();
    setDemoImages(images);

    document.documentElement.classList.remove('mocha-theme', 'latte-theme');
    document.documentElement.classList.add(`${theme}-theme`);
  }, [theme]);

  // Handle clearing the canvas
  const handleClearCanvas = () => {
    canvasRef.current?.clearCanvas();
    setIsDownloadable(false);
    showToast({ message: 'Canvas cleared!', theme });
  };

  // Handle downloading the canvas
  const handleDownloadCanvas = () => {
    if (!isDownloadable) {
      showToast({ message: 'Please draw something first.', theme });
    } else {
      canvasRef.current?.downloadCanvas();
    }
  };

  // Periodically check if the canvas has a drawing
  useEffect(() => {
    const interval = setInterval(() => {
      if (canvasRef.current) {
        setIsDownloadable(canvasRef.current.hasDrawing());
      }
    }, 100);
    return () => clearInterval(interval);
  }, []);

  // Handle loading state with messages and progress
  useEffect(() => {
    if (isLoading) {
      let firstTimeout: number;
      let subsequentInterval: number;

      firstTimeout = window.setTimeout(() => {
        setMessageIndex(1);
        setProgress(18);

        subsequentInterval = window.setInterval(() => {
          setMessageIndex((prevIndex) => (prevIndex + 1) % messages.length);
          setProgress((prevProgress) => Math.min(prevProgress + 18, 100));
        }, 5000);
      }, 3000);

      return () => {
        clearTimeout(firstTimeout);
        clearInterval(subsequentInterval);
      };
    }
  }, [isLoading, messages.length]);

  // Handle form submission to generate the story
  const handleSubmit = async () => {
    const canvasData = canvasRef.current?.getBase64FromCanvas();

    if (canvasData) {
      setIsLoading(true);
      setMessageIndex(0);
      setProgress(0);

      try {
        const response = await fetch('/infer/sketchclassify', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            image_base64: canvasData,
          }),
        });

        if (response.ok) {
          const result = await response.json();
          if (result.audio) {
            setAudioData(result.audio);
          } else {
            showToast({ message: 'No audio returned from server.', theme });
          }
        } else {
          console.error('Submission failed:', response.status, response.statusText);
          showToast({ message: `Submission failed with status ${response.status}.`, theme });
        }
      } catch (error) {
        console.error('Error submitting data:', error);
        showToast({ message: 'Network error.', theme });
      } finally {
        setIsLoading(false);
      }
    } else {
      showToast({ message: 'Canvas is empty.', theme });
    }
  };

  // Define the floating animation for bubbles
  const floatingAnimation = useSpring({
    from: { transform: 'translateY(0px) scale(1)' },
    to: async (next) => {
      while (true) {
        await next({ transform: 'translateY(-20px) scale(1.05)' });
        await next({ transform: 'translateY(20px) scale(0.95)' });
      }
    },
    config: { duration: 4000 },
    reset: true,
    loop: true,
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
        <div className="floating-bubbles">
          {demoImages.map((image, index) => (
            <animated.div
              key={index}
              className="bubble"
              style={{
                ...floatingAnimation,
                backgroundImage: `url(${image})`,
                backgroundSize: 'cover',
                backgroundPosition: 'center',
                width: '150px', // Increased from '50px' to '80px'
                height: '150px', // Increased from '50px' to '80px'
                borderRadius: '50%',
                margin: '10px', // Increased from '10px' to '15px'
              }}
            />
          ))}
        </div>

        <DrawingCanvas ref={canvasRef} />

        <div className="button-container">
          <button onClick={handleDownloadCanvas} disabled={!isDownloadable}>
            Download
          </button>
          <button onClick={handleClearCanvas}>Clear</button>
          <button onClick={handleSubmit} disabled={isLoading}>
            Generate Story
          </button>
        </div>

        <div className="audio-player-section">
          {isLoading ? (
            <div className="loader">
              <div className="progress-bar-container">
                <div
                  className="progress-bar"
                  style={{ width: `${progress}%` }}
                ></div>
              </div>
              <p>{messages[messageIndex]}</p>
            </div>
          ) : audioData ? (
            <>
              <h2>Generated Story</h2>
              <AudioPlayer theme={theme} audioData={audioData} />
            </>
          ) : null}
        </div>
      </main>

      <CustomToastContainer />

      <footer className="app-footer">
        <p>Made with ❤️ with React and Catppuccin</p>
        <p>© 2024 bedtime.ai</p>
      </footer>
    </div>
  );
};

export default App;
