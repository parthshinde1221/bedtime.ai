import '../styles/DrawingCanvas.css';
import React, { useRef, useState, useEffect, forwardRef, useImperativeHandle } from 'react';

export type DrawingCanvasHandle = {
  clearCanvas: () => void;
  downloadCanvas: () => void;
  hasDrawing: () => boolean;
  getCanvasData: () => string | null; // Add this line
  getBase64FromCanvas: () => string | null;
};

const DrawingCanvas = forwardRef<DrawingCanvasHandle>((_, ref) => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const [isDrawing, setIsDrawing] = useState(false);
  const [context, setContext] = useState<CanvasRenderingContext2D | null>(null);

  useEffect(() => {
    if (canvasRef.current) {
      const ctx = canvasRef.current.getContext('2d');
      if (ctx) {
        ctx.lineWidth = 2;
        ctx.lineCap = 'round';
        ctx.strokeStyle = '#000000';
        setContext(ctx);
      }
    }
  }, []);

  useImperativeHandle(ref, () => ({
    clearCanvas() {
      if (context && canvasRef.current) {
        context.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);
      }
    },
    downloadCanvas() {
      if (!canvasRef.current) return;

      const canvas = canvasRef.current;
      const tempCanvas = document.createElement('canvas');
      tempCanvas.width = canvas.width;
      tempCanvas.height = canvas.height;
      const tempContext = tempCanvas.getContext('2d');

      if (tempContext) {
        tempContext.fillStyle = '#ffffff';
        tempContext.fillRect(0, 0, tempCanvas.width, tempCanvas.height);
        tempContext.drawImage(canvas, 0, 0);

        const link = document.createElement('a');
        link.href = tempCanvas.toDataURL('image/png');
        link.download = 'drawing.png';
        link.click();
      }
    },
    hasDrawing() {
      if (!canvasRef.current) return false;
      const pixelBuffer = new Uint32Array(
        context!.getImageData(0, 0, canvasRef.current.width, canvasRef.current.height).data.buffer
      );
      return !pixelBuffer.every((pixel) => pixel === 0); // Check if any pixel is not empty
    },
    getCanvasData() {
      return canvasRef.current ? canvasRef.current.toDataURL('image/png') : null;
    },
    getBase64FromCanvas() {
        if (!canvasRef.current) {
          console.error("Canvas reference is not available.");
          return null;
        }
      
        const canvas = canvasRef.current;
        const tempCanvas = document.createElement('canvas');
        tempCanvas.width = canvas.width;
        tempCanvas.height = canvas.height;
        const tempContext = tempCanvas.getContext('2d');
      
        if (!tempContext) {
          console.error("Temporary canvas context is not available.");
          return null;
        }
      
        // Fill temp canvas with a white background
        tempContext.fillStyle = '#ffffff';
        tempContext.fillRect(0, 0, tempCanvas.width, tempCanvas.height);
      
        // Draw the actual content on top
        tempContext.drawImage(canvas, 0, 0);
      
        // Convert temp canvas to base64
        try {
          const dataURL = tempCanvas.toDataURL('image/png');
          return dataURL.replace(/^data:image\/png;base64,/, '');
        } catch (error) {
          console.error("Error encoding canvas to base64:", error);
          return null;
        }
      
      
    }
    
  }));

  const startDrawing = (event: React.MouseEvent) => {
    if (context) {
      context.beginPath();
      context.moveTo(event.nativeEvent.offsetX, event.nativeEvent.offsetY);
      setIsDrawing(true);
    }
  };

  const draw = (event: React.MouseEvent) => {
    if (!isDrawing || !context) return;
    context.lineTo(event.nativeEvent.offsetX, event.nativeEvent.offsetY);
    context.stroke();
  };

  const stopDrawing = () => {
    if (isDrawing) {
      context?.closePath();
      setIsDrawing(false);
    }
  };

  return (
    <div className="canvas-container">
      <canvas
        ref={canvasRef}
        width={500}
        height={500}
        onMouseDown={startDrawing}
        onMouseMove={draw}
        onMouseUp={stopDrawing}
        onMouseLeave={stopDrawing}
        className="custom-canvas"
      />
    </div>
  );
});

export default DrawingCanvas;
