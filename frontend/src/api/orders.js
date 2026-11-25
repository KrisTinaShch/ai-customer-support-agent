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

export async function cancelOrder(orderNumber, confirmed) {
  const normalizedOrderNumber = orderNumber.trim().toUpperCase()

  const response = await fetch(
    `${API_BASE_URL}/orders/${encodeURIComponent(normalizedOrderNumber)}/cancel`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        confirmed,
      }),
    },
  )

  if (!response.ok) {
    if (response.status === 400) {
      throw new Error('CONFIRMATION_REQUIRED')
    }

    if (response.status === 404) {
      throw new Error('ORDER_NOT_FOUND')
    }

    if (response.status === 409) {
      throw new Error('CANCELLATION_NOT_ALLOWED')
    }

    throw new Error('CANCELLATION_REQUEST_FAILED')
  }

  return response.json()
}
