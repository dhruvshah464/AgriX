export default function Card({ children, className = '', padding = 'p-5', hover = true, onClick, id }) {
  return (
    <div
      id={id}
      className={`bg-white rounded-xl border border-slate-100 shadow-card transition-all duration-200 ${
        hover ? 'hover:shadow-card-hover' : ''
      } ${onClick ? 'cursor-pointer hover:-translate-y-0.5' : ''} ${padding} ${className}`}
      onClick={onClick}
      role={onClick ? 'button' : undefined}
      tabIndex={onClick ? 0 : undefined}
      onKeyDown={onClick ? (e) => e.key === 'Enter' && onClick() : undefined}
    >
      {children}
    </div>
  );
}
