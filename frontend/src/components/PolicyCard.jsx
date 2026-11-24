function PolicyCard({ policy, language }) {
  return (
    <article className="policy-card">
      <h3>{policy.title[language]}</h3>
      <p>{policy.description[language]}</p>
    </article>
  )
}

export default PolicyCard
