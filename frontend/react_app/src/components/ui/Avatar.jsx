const colors = {
  green:  'bg-green-100 text-green-700',
  blue:   'bg-blue-100 text-blue-700',
  amber:  'bg-amber-100 text-amber-700',
  slate:  'bg-slate-100 text-slate-600',
  rose:   'bg-rose-100 text-rose-600',
  teal:   'bg-teal-100 text-teal-700',
};

export default function Avatar({ name, src, size = 'md', color = 'green', className = '' }) {
  const sizes = { sm: 'w-8 h-8 text-xs', md: 'w-10 h-10 text-sm', lg: 'w-12 h-12 text-base', xl: 'w-16 h-16 text-lg' };
  const initials = name
    ? name.split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase()
    : '?';

  if (src) {
    return (
      <img
        src={src}
        alt={name || 'Avatar'}
        className={`${sizes[size]} rounded-full object-cover ring-2 ring-white ${className}`}
      />
    );
  }

  return (
    <div
      className={`${sizes[size]} ${colors[color]} rounded-full flex items-center justify-center font-semibold ring-2 ring-white ${className}`}
      title={name}
    >
      {initials}
    </div>
  );
}
