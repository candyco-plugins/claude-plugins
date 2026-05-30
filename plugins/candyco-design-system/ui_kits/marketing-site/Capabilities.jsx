function CapabilityCard({ icon, title, body }) {
  return (
    <div className="ms-cap-card">
      <div className="ms-cap-icon">
        <i data-lucide={icon} style={{ width: 22, height: 22, strokeWidth: 1.5 }}></i>
      </div>
      <h3>{title}</h3>
      <p>{body}</p>
    </div>
  );
}

function Capabilities() {
  const caps = [
    { icon: "factory", title: "Twelve owned plants", body: "Vertically integrated production across hard candy, chocolate, gummies, panned, and seasonal lines." },
    { icon: "boxes", title: "Spec to shelf in 90 days", body: "Formulation, packaging, regulatory, and first-run samples on a single timeline." },
    { icon: "truck", title: "Allocated logistics", body: "Dedicated DC-direct lanes for top-six retailers. No brokers, no surprise freight." },
    { icon: "shield-check", title: "GFSI · Kosher · Halal", body: "Audit-ready by default. SQF Level 3 across every plant, with annual third-party reviews." },
    { icon: "line-chart", title: "Forecast-locked capacity", body: "Quarterly allocation windows let buyers reserve runs eighteen months out." },
    { icon: "clipboard-check", title: "Private-label first", body: "Every line we own is built for someone else's label. We do not compete with our partners." },
  ];
  return (
    <section className="ms-section" id="capabilities">
      <div className="ms-container">
        <div className="ms-section-head">
          <div className="ms-eyebrow" style={{ color: "var(--shadow-grey-500)" }}>Capabilities</div>
          <h2>The boring parts, handled.</h2>
          <p>You bring the brand and the buy. We bring the plants, the people, and the paperwork. No surprises between PO and pallet.</p>
        </div>
        <div className="ms-cap-grid">
          {caps.map((c, i) => <CapabilityCard key={i} {...c} />)}
        </div>
      </div>
    </section>
  );
}
window.Capabilities = Capabilities;
