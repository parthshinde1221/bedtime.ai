import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

type CustomToastProps = {
  message: string;
  theme: 'mocha' | 'latte';
};

export const showToast = ({ message, theme }: CustomToastProps) => {
  toast(message, {
    position: "bottom-center",
    autoClose: 2000,
    hideProgressBar: true,
    closeOnClick: true,
    pauseOnHover: false,
    draggable: true,
    style: {
      backgroundColor: theme === 'mocha' ? '#181825' : '#e6e9ef',
      color: theme === 'mocha' ? '#cdd6f4' : '#4c4f69',
    },
  });
};

export const CustomToastContainer = () => (
  <ToastContainer />
);
