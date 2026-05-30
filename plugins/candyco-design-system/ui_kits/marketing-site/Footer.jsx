function Footer() {
  const cols = [
    { h: "Capabilities", links: ["Hard candy", "Chocolate", "Gummies", "Panned & coated", "Seasonal"] },
    { h: "Partners",     links: ["Buyer onboarding", "Capacity calendar", "Spec library", "Logistics"] },
    { h: "Company",      links: ["About", "Plants", "Press", "Careers"] },
  ];
  return (
    <footer className="ms-footer">
      <div className="ms-container">
        <div className="ms-footer-grid">
          <div>
            <img src="../../assets/logo/candyco-logo-white.png" alt="CandyCo" style={{ height: 56 }} />
            <p className="ms-footer-tag">
              The full-scale confectionary partner behind the brands you already buy.
            </p>
          </div>
          {cols.map(c => (
            <div key={c.h}>
              <h4>{c.h}</h4>
              <ul>{c.links.map(l => <li key={l}><a href="#">{l}</a></li>)}</ul>
            </div>
          ))}
        </div>
        <div className="ms-footer-legal">
          <span>© 2026 CandyCo Inc. All rights reserved.</span>
          <span style={{ display: "flex", gap: 24 }}>
            <a href="#">Privacy</a>
            <a href="#">Terms</a>
            <a href="#">Compliance</a>
          </span>
        </div>
      </div>
    </footer>
  );
}
window.Footer = Footer;
