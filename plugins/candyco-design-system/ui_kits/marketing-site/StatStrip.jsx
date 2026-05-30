function StatStrip() {
  const stats = [
    { eb: "Plants", num: "12", label: "Coast to coast, GFSI certified" },
    { eb: "Annual run rate", num: <span>1.4<span style={{ color: "var(--racing-red)" }}>B</span></span>, label: "Units shipped, FY24" },
    { eb: "On-time ship", num: "98.7%", label: "Across 4,200 launches" },
    { eb: "Retail partners", num: "6", label: "Top-10 US grocers" },
  ];
  return (
    <section className="ms-stats">
      <div className="ms-container ms-stats-grid">
        {stats.map((s, i) => (
          <div key={i} className="ms-stat">
            <div className="ms-eyebrow">{s.eb}</div>
            <div className="ms-stat-num">{s.num}</div>
            <div className="ms-stat-label">{s.label}</div>
          </div>
        ))}
      </div>
    </section>
  );
}
window.StatStrip = StatStrip;
