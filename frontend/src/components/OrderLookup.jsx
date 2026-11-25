import { useState } from 'react'
import { cancelOrder, getOrder } from '../api/orders.js'

function OrderLookup({ text }) {
  const [orderNumber, setOrderNumber] = useState('')
  const [order, setOrder] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [errorCode, setErrorCode] = useState(null)
  const [isConfirmingCancellation, setIsConfirmingCancellation] =
    useState(false)
  const [isCanceling, setIsCanceling] = useState(false)
  const [wasCanceled, setWasCanceled] = useState(false)

  const handleSubmit = async (event) => {
    event.preventDefault()

    setIsLoading(true)
    setOrder(null)
    setErrorCode(null)
    setIsConfirmingCancellation(false)
    setIsCanceling(false)
    setWasCanceled(false)

    try {
      const foundOrder = await getOrder(orderNumber)
      setOrder(foundOrder)
    } catch (error) {
      const nextErrorCode =
        error instanceof Error && error.message === 'ORDER_NOT_FOUND'
          ? 'ORDER_NOT_FOUND'
          : 'ORDER_REQUEST_FAILED'

      setErrorCode(nextErrorCode)
    } finally {
      setIsLoading(false)
    }
  }
  const handleCancelOrder = async () => {
    setIsCanceling(true)
    setErrorCode(null)
    setWasCanceled(false)

    try {
      const canceledOrder = await cancelOrder(order.order_number, true)

      setOrder(canceledOrder)
      setIsConfirmingCancellation(false)
      setWasCanceled(true)
    } catch (error) {
      const knownErrorCodes = [
        'CONFIRMATION_REQUIRED',
        'ORDER_NOT_FOUND',
        'CANCELLATION_NOT_ALLOWED',
        'CANCELLATION_REQUEST_FAILED',
      ]

      const nextErrorCode =
        error instanceof Error && knownErrorCodes.includes(error.message)
          ? error.message
          : 'CANCELLATION_REQUEST_FAILED'

      setErrorCode(nextErrorCode)
    } finally {
      setIsCanceling(false)
    }
  }
  return (
    <section className="order-section" id="order" aria-labelledby="order-title">
      <div className="section-heading">
        <p className="eyebrow">{text.eyebrow}</p>
        <h2 id="order-title">{text.title}</h2>
        <p>{text.description}</p>
      </div>

      <form className="order-form" onSubmit={handleSubmit}>
        <label htmlFor="order-number">{text.label}</label>

        <input
          id="order-number"
          name="orderNumber"
          type="text"
          value={orderNumber}
          onChange={(event) => setOrderNumber(event.target.value)}
          placeholder={text.placeholder}
          autoComplete="off"
          required
        />

        <button type="submit" disabled={isLoading}>
          {isLoading ? text.loading : text.submit}
        </button>

        <p className="order-hint">{text.hint}</p>
        {errorCode && (
          <p className="order-error" role="alert">
            {text.errors[errorCode]}
          </p>
        )}
        {order && (
          <div className="order-result" role="status">
            <h3>{text.resultTitle}</h3>

            <p>
              <strong>{text.orderNumber}:</strong> {order.order_number}
            </p>

            <p>
              <strong>{text.status}:</strong> {text.statuses[order.status]}
            </p>

            <p
              className={
                order.can_be_canceled
                  ? 'order-availability is-available'
                  : 'order-availability is-unavailable'
              }
            >
              {order.can_be_canceled ? text.canCancel : text.cannotCancel}
            </p>

            {order.can_be_canceled && !isConfirmingCancellation && (
              <button
                type="button"
                className="cancel-action"
                onClick={() => setIsConfirmingCancellation(true)}
              >
                {text.cancelAction}
              </button>
            )}

            {order.can_be_canceled && isConfirmingCancellation && (
              <div className="cancel-confirmation">
                <p>{text.cancelQuestion}</p>

                <div className="confirmation-actions">
                  <button
                    type="button"
                    onClick={() => setIsConfirmingCancellation(false)}
                  >
                    {text.keepOrder}
                  </button>

                  <button
                    type="button"
                    onClick={handleCancelOrder}
                    disabled={isCanceling}
                  >
                    {isCanceling ? text.canceling : text.confirmCancel}
                  </button>
                </div>
              </div>
            )}
            {wasCanceled && (
              <p className="order-success">{text.canceledSuccess}</p>
            )}
          </div>
        )}
      </form>
    </section>
  )
}

export default OrderLookup
