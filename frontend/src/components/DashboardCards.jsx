function DashboardCards({ stats }) {
  const cards = [
    {
      title: "Total Records",
      value: stats.total_records,
      tone: "from-emerald-500/20 to-emerald-100",
    },
    {
      title: "Pending",
      value: stats.pending_records,
      tone: "from-amber-500/25 to-amber-100",
    },
    {
      title: "Approved",
      value: stats.approved_records,
      tone: "from-sky-500/20 to-sky-100",
    },
    {
      title: "Suspicious",
      value: stats.suspicious_records,
      tone: "from-rose-500/20 to-rose-100",
    },
  ];

  return (
    <div className="rise grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-4">
      {cards.map((card, index) => (
        <div
          key={index}
          className="glass-panel rounded-3xl p-6"
        >
          <div className={`mb-4 h-2 w-20 rounded-full bg-gradient-to-r ${card.tone}`} />
          <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-500">
            {card.title}
          </h3>
          <p className="mt-2 text-4xl font-extrabold text-slate-800">
            {card.value}
          </p>
        </div>
      ))}
    </div>
  );
}

export default DashboardCards;
