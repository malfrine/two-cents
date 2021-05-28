import { InstrumentColorManager, InstrumentIconManager } from '~/assets/instruments'

export default ({ app }, inject) => {
  // Inject $hello(msg) in Vue, context and store.
  inject('instrument', {
    colors: new InstrumentColorManager(),
    icons: new InstrumentIconManager()
  })
}
