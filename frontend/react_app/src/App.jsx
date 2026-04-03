import { RouterProvider } from 'react-router-dom';
import { router } from './routes/router';
import { AppProvider } from './context/AppContext';

export default function App() {
  return (
    <AppProvider>
      <RouterProvider router={router} />
    </AppProvider>
  );
}
