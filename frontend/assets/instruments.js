import { LOAN_COLORS, INVESTMENT_COLORS, COLORS, ColorGetter } from './colors'

class InstrumentColorGetter {
    colors = {}
    colorGetter = new ColorGetter()

    constructor (colors = COLORS) {
      this.colorGetter = new ColorGetter(colors)
    }

    getColor (instrumentId) {
      let color = this.colors[instrumentId]
      if (!color) {
        color = this.colorGetter.getNextColor()
        this.colors[instrumentId] = color
      }
      return color
    }
}

const loanColors = new InstrumentColorGetter(LOAN_COLORS)
const investmentColors = new InstrumentColorGetter(INVESTMENT_COLORS)
const defaultColors = new InstrumentColorGetter(COLORS)

class InstrumentColorManager {
  constructor () {
    this.colors = {
      loan: loanColors,
      investment: investmentColors,
      default: defaultColors
    }
  }

  getColor (type, id) {
    const instrumentColorGetter = this.colors[type] || this.colors.default
    return instrumentColorGetter.getColor(id)
  }
}

class InstrumentIconManager {
  constructor () {
    this.icons = {
      Mortgage: 'mdi-home',
      'Student Line of Credit': 'mdi-school',
      'Student Loan': 'mdi-school',
      'Line of Credit': 'mdi-bank',
      'Credit Card': 'mdi-credit-card',
      'Car Loan': 'mdi-car',
      'Personal Loan': 'mdi-bank',
      ETF: 'mdi-trending-up',
      'Mutual Fund': 'mdi-trending-up',
      GIC: 'mdi-gift',
      'Term Deposit': 'mdi-gift',
      Stock: 'mdi-rocket',
      Cash: 'mdi-cash',
      'Nest Egg': 'mdi-shield',
      'Big Purchase': 'mdi-gift'
    }
  }

  getIcon (type) {
    return this.icons[type]
  }
}

export { InstrumentColorManager, InstrumentIconManager }
