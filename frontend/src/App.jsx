import ProductCard from './components/ProductCard.jsx'
import { products } from './data/products.js'
import './App.css'

function App() {
  const language = 'en'

  return (
    <div className="app">
      <header className="site-header">
        <a className="brand" href="#top">
          Luma Store
        </a>

        <nav className="main-navigation" aria-label="Main navigation">
          <a href="#products">Products</a>
          <a href="#policies">Policies</a>
          <a href="#order">Track order</a>
        </nav>

        <span className="demo-badge">Demo store</span>
      </header>

      <main id="top">
        <section className="hero-section" aria-labelledby="hero-title">
          <p className="eyebrow">Photography essentials</p>

          <h1 id="hero-title">Tools for every frame.</h1>

          <p className="hero-description">
            Studio lighting, backgrounds, and accessories for photographers who
            care about every detail.
          </p>

          <a className="primary-link" href="#products">
            Shop the collection
          </a>
        </section>

        <section
          className="products-section"
          id="products"
          aria-labelledby="products-title"
        >
          <div className="section-heading">
            <p className="eyebrow">Selected gear</p>
            <h2 id="products-title">Built for the studio and the road.</h2>
            <p>
              Reliable essentials for lighting, shooting, and protecting your
              work.
            </p>
          </div>

          <div className="product-grid">
            {products.map((product) => (
              <ProductCard
                key={product.id}
                product={product}
                language={language}
              />
            ))}
          </div>
        </section>
      </main>
    </div>
  )
}

export default App
