import { RouterProvider } from 'react-router-dom';
import { router } from './routes/router';
import { AppProvider } from './context/AppContext';
import { AuthProvider } from './context/AuthContext';

export default function App() {
  return (
    <AuthProvider>
      <AppProvider>
        <RouterProvider router={router} />
      </AppProvider>
    </AuthProvider>
  );
}
