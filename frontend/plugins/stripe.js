export default ({ env: { stripePublishableKey } }, inject) => {
  // eslint-disable-next-line no-undef
  const stripe = Stripe(stripePublishableKey)
  inject('stripe', stripe)
}
