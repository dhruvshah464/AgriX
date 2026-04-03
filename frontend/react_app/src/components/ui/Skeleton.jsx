export default function Skeleton({ className = '', variant = 'rect', width, height, count = 1 }) {
  const base = 'skeleton';
  const styles = {
    rect: `${base} rounded-lg`,
    circle: `${base} rounded-full`,
    text: `${base} rounded h-4`,
    card: `${base} rounded-xl`,
  };

  const items = Array.from({ length: count }, (_, i) => (
    <div
      key={i}
      className={`${styles[variant] || styles.rect} ${className}`}
      style={{ width, height }}
    />
  ));

  return count === 1 ? items[0] : <div className="space-y-3">{items}</div>;
}

export function SkeletonCard() {
  return (
    <div className="bg-white rounded-xl border border-slate-100 p-5 space-y-4">
      <div className="flex items-center gap-3">
        <Skeleton variant="circle" width={40} height={40} />
        <div className="flex-1 space-y-2">
          <Skeleton width="60%" height={14} />
          <Skeleton width="40%" height={12} />
        </div>
      </div>
      <Skeleton height={20} />
      <Skeleton width="75%" height={12} />
    </div>
  );
}

export function SkeletonChart() {
  return (
    <div className="bg-white rounded-xl border border-slate-100 p-5 space-y-4">
      <Skeleton width="40%" height={18} />
      <Skeleton height={200} variant="card" />
    </div>
  );
}
