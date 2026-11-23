import './App.css'

function App() {
    return(
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
                Studio lighting, backgrounds, and accessories for photographers
                who care about every detail.
              </p>

              <a className="primary-link" href="#products">
                Shop the collection
              </a>
            </section>
          </main>
        </div>
    )
}

export default App