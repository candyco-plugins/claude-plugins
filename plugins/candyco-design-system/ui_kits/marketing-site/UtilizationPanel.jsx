function UtilizationPanel() {
  const rows = [
    { plant: "Plant 03 · Memphis",   line: "Hard candy",  pct: 32, tier: "ramping" },
    { plant: "Plant 07 · Boise",     line: "Gummies",     pct: 58, tier: "growing" },
    { plant: "Plant 11 · Denver",    line: "Chocolate",   pct: 64, tier: "growing" },
    { plant: "Plant 12 · Allentown", line: "Panned",      pct: 82, tier: "approaching" },
    { plant: "Plant 04 · Reno",      line: "Seasonal",    pct: 96, tier: "full" },
  ];
  const tiers = {
    ramping:     { color: "#1982C4", bg: "#E3F1FB", fg: "#0B5180", label: "Ramping" },
    growing:     { color: "#23CE6B", bg: "#E8FAF0", fg: "#176B3A", label: "Growing" },
    approaching: { color: "#FFCA3A", bg: "#FFF7DB", fg: "#7A5800", label: "Approaching" },
    full:        { color: "#FF0022", bg: "#FFE5E9", fg: "#A30016", label: "At capacity" },
  };
  return (
    <section className="ms-section ms-section-bg" id="capacity">
      <div className="ms-container">
        <div className="ms-section-head">
          <div className="ms-eyebrow" style={{ color: "var(--shadow-grey-500)" }}>Capacity, live</div>
          <h2>Reserve a line before your competitor does.</h2>
          <p>Q3 allocation closes August 1. Below: current utilization across every owned plant. Slots ramping today open the most flexible specs.</p>
        </div>
        <div className="ms-util-panel">
          <div className="ms-util-head">
            <h3>FY26 Q3 · Plant utilization</h3>
            <span style={{ fontFamily: "var(--font-mono)", fontSize: 12, color: "var(--fg-3)" }}>
              Updated 14:32 ET · Auto-refresh
            </span>
          </div>
          {rows.map((r, i) => {
            const t = tiers[r.tier];
            return (
              <div key={i} className="ms-util-row">
                <div className="ms-util-plant">
                  <i data-lucide="factory" style={{ width: 16, height: 16, strokeWidth: 1.5, color: "var(--fg-2)" }}></i>
                  <span>{r.plant}</span>
                  <span style={{ fontSize: 12, color: "var(--fg-3)", fontWeight: 400, marginLeft: 6 }}>· {r.line}</span>
                </div>
                <div className="ms-util-bar">
                  <div className={`ms-util-bar-fill ${r.tier}`} style={{ width: `${r.pct}%` }}></div>
                </div>
                <div className="ms-util-pct" style={{ color: t.fg }}>{r.pct}%</div>
                <span className="ms-util-cap" style={{ background: t.bg, color: t.fg }}>
                  <span className="dot" style={{ background: t.color }}></span>
                  {t.label}
                </span>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
window.UtilizationPanel = UtilizationPanel;
