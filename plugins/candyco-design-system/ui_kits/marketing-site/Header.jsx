/* global React */
const { useState, useEffect } = React;

function Header() {
  const [scrolled, setScrolled] = useState(false);
  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 8);
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);
  return (
    <header className="ms-header" style={{ boxShadow: scrolled ? "0 1px 0 rgba(39,40,56,0.08)" : "none" }}>
      <div className="ms-container ms-header-inner">
        <a href="#" style={{ display: "flex", alignItems: "center" }}>
          <img src="../../assets/logo/candyco-logo-black.png" alt="CandyCo" style={{ height: 44 }} />
        </a>
        <nav className="ms-nav">
          <a href="#capabilities">Capabilities</a>
          <a href="#capacity">Capacity</a>
          <a href="#partners">Partners</a>
          <a href="#about">About</a>
        </nav>
        <div className="ms-header-cta">
          <a href="#" style={{ fontSize: 14, fontWeight: 500, color: "var(--fg-1)", textDecoration: "none" }}>Sign in</a>
          <a href="#" className="ms-btn ms-btn-primary">Request capacity</a>
        </div>
      </div>
    </header>
  );
}
window.Header = Header;
