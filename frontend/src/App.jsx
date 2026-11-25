import { useState } from 'react'
import OrderLookup from './components/OrderLookup.jsx'
import ProductCard from './components/ProductCard.jsx'
import PolicyCard from './components/PolicyCard.jsx'
import { products } from './data/products.js'
import { policies } from './data/policies.js'
import { translations } from './data/translations.js'
import './App.css'

function App() {
  const [language, setLanguage] = useState('en')
  const text = translations[language]

  const handleLanguageChange = () => {
    setLanguage((currentLanguage) => (currentLanguage === 'en' ? 'bg' : 'en'))
  }

  return (
    <div className="app">
      <header className="site-header">
        <a className="brand" href="#top">
          Luma Store
        </a>

        <nav className="main-navigation" aria-label={text.navigation.label}>
          <a href="#products">{text.navigation.products}</a>
          <a href="#policies">{text.navigation.policies}</a>
          <a href="#order">{text.navigation.trackOrder}</a>
        </nav>
        <span className="demo-badge">{text.demoStore}</span>
        <button
          className="language-toggle"
          type="button"
          onClick={handleLanguageChange}
          aria-label={text.switchLanguage}
        >
          {language === 'en' ? 'BG' : 'EN'}
        </button>
      </header>

      <main id="top">
        <section className="hero-section" aria-labelledby="hero-title">
          <p className="eyebrow">{text.hero.eyebrow}</p>

          <h1 id="hero-title">{text.hero.title}</h1>

          <p className="hero-description">{text.hero.description}</p>

          <a className="primary-link" href="#products">
            {text.hero.action}
          </a>
        </section>

        <section
          className="products-section"
          id="products"
          aria-labelledby="products-title"
        >
          <div className="section-heading">
            <p className="eyebrow">{text.catalog.eyebrow}</p>
            <h2 id="products-title">{text.catalog.title}</h2>
            <p>{text.catalog.description}</p>
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
        <section
          className="policies-section"
          id="policies"
          aria-labelledby="policies-title"
        >
          <div className="section-heading">
            <p className="eyebrow">{text.policiesSection.eyebrow}</p>
            <h2 id="policies-title">{text.policiesSection.title}</h2>
            <p>{text.policiesSection.description}</p>
          </div>

          <div className="policy-grid">
            {policies.map((policy) => (
              <PolicyCard key={policy.id} policy={policy} language={language} />
            ))}
          </div>
        </section>
        <OrderLookup text={text.orderLookup} />
      </main>
    </div>
  )
}

export default App
