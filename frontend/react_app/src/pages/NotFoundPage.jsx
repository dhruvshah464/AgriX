import { Link } from 'react-router-dom';
import { Home, Leaf } from 'lucide-react';

export default function NotFoundPage() {
  return (
    <div className="min-h-[70vh] flex flex-col items-center justify-center text-center px-6">
      <div className="w-20 h-20 rounded-2xl bg-green-50 flex items-center justify-center mb-6">
        <Leaf size={36} className="text-green-500" />
      </div>
      <h1 className="text-6xl font-bold text-slate-200 mb-2">404</h1>
      <h2 className="text-xl font-semibold text-slate-800 mb-2">Page not found</h2>
      <p className="text-sm text-slate-500 max-w-md mb-8">
        The field you're looking for doesn't exist in our records. It may have been harvested or moved.
      </p>
      <Link
        to="/"
        className="inline-flex items-center gap-2 px-5 py-2.5 bg-green-600 hover:bg-green-700 text-white text-sm font-medium rounded-lg transition-all shadow-sm hover:shadow-md active:scale-[0.97]"
      >
        <Home size={16} />
        Back to Dashboard
      </Link>
    </div>
  );
}
