function ProductCard({ product, language }) {
  const locale = language === 'bg' ? 'bg-BG' : 'en-IE'

  const formattedPrice = new Intl.NumberFormat(locale, {
    style: 'currency',
    currency: product.currency,
  }).format(product.price)
  return (
    <article className="product-card">
      <div className="product-visual">
        <img src={product.image} alt={product.name[language]} loading="lazy" />
      </div>

      <div className="product-content">
        <p className="product-category">{product.category[language]}</p>
        <h3>{product.name[language]}</h3>
        <p className="product-description">{product.description[language]}</p>
        <p className="product-price">{formattedPrice}</p>
      </div>
    </article>
  )
}
export default ProductCard
