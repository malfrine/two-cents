
export default ({ app }, inject) => {
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
