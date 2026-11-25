const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000'

export async function getOrder(orderNumber) {
  const normalizedOrderNumber = orderNumber.trim().toUpperCase()

  const response = await fetch(
    `${API_BASE_URL}/orders/${encodeURIComponent(normalizedOrderNumber)}`,
  )

  if (!response.ok) {
    if (response.status === 404) {
      throw new Error('ORDER_NOT_FOUND')
    }
    throw new Error('ORDER_REQUEST_FAILED')
  }
  return response.json()
}
