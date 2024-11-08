import { useRef, useState, useEffect } from 'react';
import { showToast } from './CustomToast';
import 'react-toastify/dist/ReactToastify.css';

type AudioPlayerProps = {
  theme: 'mocha' | 'latte';
};

const AudioPlayer = ({ theme }: AudioPlayerProps) => {
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);

  const playAudio = () => {
    audioRef.current?.play();
    setIsPlaying(true);
    showToast({ message: 'Good Boy!', theme });
  };

  const pauseAudio = () => {
    audioRef.current?.pause();
    setIsPlaying(false);
  };

  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;

    const updateCurrentTime = () => setCurrentTime(audio.currentTime);
    const handleEnded = () => setIsPlaying(false);

    audio.addEventListener('loadedmetadata', () => setDuration(audio.duration));
    audio.addEventListener('timeupdate', updateCurrentTime);
    audio.addEventListener('ended', handleEnded);

    return () => {
      audio.removeEventListener('timeupdate', updateCurrentTime);
      audio.removeEventListener('ended', handleEnded);
    };
  }, []);

  const handleSeek = (event: React.ChangeEvent<HTMLInputElement>) => {
    const time = parseFloat(event.target.value);
    if (audioRef.current) {
      audioRef.current.currentTime = time;
      setCurrentTime(time);
    }
  };

  return (
    <div className="audio-player">
      <audio ref={audioRef} src="src/assets/a.mp3"></audio>

      <div className="controls">
        <button onClick={isPlaying ? pauseAudio : playAudio}>
          {isPlaying ? 'Pause' : 'Play'}
        </button>

        <input
          type="range"
          min="0"
          max={duration.toString()}
          step="0.1"
          value={currentTime}
          onChange={handleSeek}
          className="seek-bar"
        />

        <div className="time">
          {Math.floor(currentTime / 60)}:{Math.floor(currentTime % 60).toString().padStart(2, '0')} / {Math.floor(duration / 60)}:{Math.floor(duration % 60).toString().padStart(2, '0')}
        </div>
      </div>

      {/* <CustomToastContainer /> */}
    </div>
  );
};

export default AudioPlayer;
