function Quote() {
  return (
    <section className="ms-section" id="partners" style={{ paddingTop: 64, paddingBottom: 64 }}>
      <div className="ms-container" style={{ maxWidth: 880 }}>
        <div className="ms-eyebrow" style={{ color: "var(--shadow-grey-500)", marginBottom: 24 }}>Partner testimonial</div>
        <blockquote style={{
          fontFamily: "'Frank Ruhl Libre', serif",
          fontWeight: 400,
          fontSize: 32,
          lineHeight: 1.35,
          color: "var(--fg-1)",
          margin: 0,
          textWrap: "balance",
        }}>
          "We've worked with CandyCo through three product launches and four holiday seasons. They never miss a ship date — and they always tell us first when capacity is going to tighten."
        </blockquote>
        <div style={{ marginTop: 24, fontSize: 14, color: "var(--fg-2)" }}>
          <strong style={{ color: "var(--fg-1)" }}>VP Merchandising</strong> · National grocery retailer
        </div>
      </div>
    </section>
  );
}

function RetailerStrip() {
  const partners = ["Costco", "Sam's Club", "Trader Joe's", "Kroger", "Walmart", "Albertsons"];
  return (
    <section className="ms-retailer-strip">
      <div className="ms-container">
        <div className="ms-eyebrow" style={{ textAlign: "center", marginBottom: 20, color: "var(--shadow-grey-500)" }}>
          Trusted by America's largest retailers
        </div>
        <div className="ms-retailer-row">
          {partners.map(p => <span key={p} className="ms-retailer-pill">{p}</span>)}
        </div>
      </div>
    </section>
  );
}
window.Quote = Quote;
window.RetailerStrip = RetailerStrip;
