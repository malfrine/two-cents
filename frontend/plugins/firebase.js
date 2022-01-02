export default function ({ $fire }) {
  // if $fire.analytics is unintialized, add a dummy events logger
  const dummyAnalytics = {
    logEvent (event, data = null) {
      return null
    }
  }
  if (!$fire.analytics) {
    $fire.analytics = dummyAnalytics
  }
}
