export default function ({ $axios, store, $fire }) {
  $axios.defaults.xsrfCookieName = 'csrftoken'
  $axios.defaults.xsrfHeaderName = 'X-CSRFToken'
  $axios.onRequest((config) => {
    if (store.state['firebase-auth'].idToken) {
      config.headers.common.AUTHORIZATION = store.state['firebase-auth'].idToken
    }
    // config.headers.common.client = store.state.user.headers.client
    // config.headers.common.expiry = store.state.user.headers.expiry
    // config.headers.common.uid = store.state.user.headers.uid
  })
}
