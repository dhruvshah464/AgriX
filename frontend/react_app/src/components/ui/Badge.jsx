const variants = {
  green:  'bg-green-50 text-green-700',
  amber:  'bg-amber-50 text-amber-700',
  red:    'bg-rose-50 text-rose-700',
  blue:   'bg-blue-50 text-blue-700',
  teal:   'bg-teal-50 text-teal-700',
  slate:  'bg-slate-100 text-slate-600',
  emerald:'bg-emerald-50 text-emerald-700',
};

export default function Badge({ children, variant = 'green', dot = false, className = '' }) {
  return (
    <span className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium tracking-wide ${variants[variant] || variants.slate} ${className}`}>
      {dot && <span className={`w-1.5 h-1.5 rounded-full bg-current opacity-70`} />}
      {children}
    </span>
  );
}
