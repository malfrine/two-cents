
export default ({ app }, inject) => {
  // Inject $hello(msg) in Vue, context and store.
  inject('constants', {
    provinces: [
      'AB',
      'BC',
      'MB',
      'NB',
      'NL',
      'NT',
      'ON',
      'PEI',
      'QB',
      'SK',
      'YK'
    ]
  })
}
