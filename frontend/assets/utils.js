const delay = ms => new Promise(resolve => setTimeout(resolve, ms))

const getFirstDayOfNextMonth = function (curDate) {
  if (curDate.getMonth() === 11) {
    return new Date(curDate.getFullYear() + 1, 0)
  } else {
    return new Date(curDate.getFullYear(), curDate.getMonth() + 1)
  }
}

const calculateMonthsBetween = function (startDate, endDate) {
  return endDate.getMonth() - startDate.getMonth() +
    (12 * (endDate.getFullYear() - startDate.getFullYear()))
}

const calculateMinimumAmortizedLoanPayment = function (principal, apr, endDate) {
  const monthlyInterestRate = apr / 100 / 12
  const months = calculateMonthsBetween(getFirstDayOfNextMonth(new Date()), endDate)
  const discountFactor = (monthlyInterestRate * (1 + monthlyInterestRate) ** months) / ((1 + monthlyInterestRate) ** months - 1)
  return Math.round(principal * discountFactor)
}

const calculateMinimumRevolvingLoanPayment = function (principal, apr) {
  return principal * apr / 12 / 100
}

const asDollar = function (num) {
  return Number(num).toLocaleString('en-CA', { style: 'currency', currency: 'CAD', minimumFractionDigits: 0 })
}

function debounce (fn, delay) {
  let timeoutID = null
  return function () {
    clearTimeout(timeoutID)
    const args = arguments
    const that = this
    timeoutID = setTimeout(function () {
      fn.apply(that, args)
    }, delay)
  }
}

function mandatoryFieldRule (requiredFields, fieldName, verboseName) {
  if (requiredFields.includes(fieldName)) {
    return v => v !== null || `Must provide ${verboseName}`
  } else {
    return v => true
  }
}

function copyToClipboard (text) {
  const el = document.createElement('textarea') // Create a <textarea> element
  el.value = text // Set its value to the string that you want copied
  el.setAttribute('readonly', '') // Make it readonly to be tamper-proof
  el.style.position = 'absolute'
  el.style.left = '-9999px' // Move outside the screen to make it invisible
  document.body.appendChild(el) // Append the <textarea> element to the HTML document
  const selected =
document.getSelection().rangeCount > 0 // Check if there is any content selected previously
  ? document.getSelection().getRangeAt(0) // Store selection if found
  : false // Mark as false to know no selection existed before
  el.select() // Select the <textarea> content
  document.execCommand('copy') // Copy - only works as a result of a user action (e.g. click events)
  document.body.removeChild(el) // Remove the <textarea> element
  if (selected) { // If a selection existed before copying
    document.getSelection().removeAllRanges() // Unselect everything on the HTML document
    document.getSelection().addRange(selected) // Restore the original selection
  }
}

const defaultTitle = 'Two Cents - DIY Financial Planning Powered by AI'
const defaultDescription = 'Everyone deserves a financial plan. At Two Cents, we help you build a free financial plan using AI. Get started today!'
const defaultTmageUrl = 'https://res.cloudinary.com/two-cents-ca/image/upload/v1619802575/og-image-bannger_dvnpka.png'
function makeSeoHeaders (title = defaultTitle, description = defaultDescription, imageUrl = defaultTmageUrl) {
  return [
    {
      hid: 'og::site_name',
      name: 'og::site_name',
      content: 'https://two-cents.ca'
    },
    {
      hid: 'twitter:title',
      name: 'twitter:title',
      content: title
    },
    {
      hid: 'twitter:description',
      name: 'twitter:description',
      content: description
    },
    {
      hid: 'twitter:image',
      name: 'twitter:image',
      content: imageUrl
    },
    {
      hid: 'twitter:image:alt',
      name: 'twitter:image:alt',
      content: title
    },
    {
      hid: 'og:title',
      property: 'og:title',
      content: title
    },
    {
      hid: 'og:description',
      property: 'og:description',
      content: description
    },
    {
      hid: 'og:image',
      property: 'og:image',
      content: imageUrl
    },
    {
      hid: 'og:image:secure_url',
      property: 'og:image:secure_url',
      content: imageUrl
    },
    {
      hid: 'og:image:alt',
      property: 'og:image:alt',
      content: title
    }
  ]
}

const RRSP_LIMIT_INCOME_FACTOR = 0.18
const RRSP_DEFAULT_FUTURE_LIMIT = 25000
const RRSP_DEFAULT_PAST_LIMIT = 10000
const RRSP_HISTORICAL_LIMITS = {
  2022: 29210,
  2021: 27830,
  2020: 27230,
  2019: 26500,
  2018: 26230,
  2017: 26010,
  2016: 25370,
  2015: 24930,
  2014: 24270,
  2013: 23820,
  2012: 22970,
  2011: 22450,
  2010: 22000,
  2009: 21000,
  2008: 20000,
  2007: 19000,
  2006: 18000,
  2005: 16500,
  2004: 15500,
  2003: 14500,
  2002: 13500,
  2001: 13500,
  2000: 13500,
  1999: 13500,
  1998: 13500,
  1997: 13500,
  1996: 13500,
  1995: 14500,
  1994: 13500,
  1993: 12500,
  1992: 12500,
  1991: 11500
}

const getRrspLimit = function (year, annualSalary) {
  let limit = RRSP_DEFAULT_FUTURE_LIMIT
  if (year > 2022) {
    limit = RRSP_DEFAULT_FUTURE_LIMIT
  } else if (year < 1991) {
    limit = RRSP_DEFAULT_PAST_LIMIT
  } else {
    limit = RRSP_HISTORICAL_LIMITS[year]
  }
  return Math.min(RRSP_LIMIT_INCOME_FACTOR * annualSalary, limit)
}

const estimateMaxRrspContributionLimit = function (workStartYear, avgAnnualSalary) {
  const thisYear = new Date().getFullYear()
  let curYear = workStartYear
  let limit = 0
  while (curYear <= thisYear) {
    limit += getRrspLimit(curYear, avgAnnualSalary)
    curYear++
  }
  return limit
}

const FUTURE_TFSA_LIMIT = 6000
const TFSA_START_AGE = 18
const HISTORICAL_TFSA_LIMITS = {
  2009: 5000,
  2010: 5000,
  2011: 5000,
  2012: 5000,
  2013: 5500,
  2014: 5500,
  2015: 10000,
  2016: 5500,
  2017: 5500,
  2018: 5500,
  2019: 6000,
  2020: 6000
}

const getTfsaLimit = function (year) {
  if (year > 2020) {
    return FUTURE_TFSA_LIMIT
  } else if (year < 1991) {
    return 0
  } else {
    return HISTORICAL_TFSA_LIMITS[year]
  }
}

const estimateMaxTfsaContributionLimit = function (birthYear) {
  const thisYear = new Date().getFullYear()
  const tfsaStartYear = birthYear + TFSA_START_AGE
  let curYear = tfsaStartYear
  let limit = 0
  while (curYear <= thisYear) {
    limit += getTfsaLimit(curYear)
    curYear++
  }
  return limit
}

const WORK_START_AGE = 23
const estimateWorkStartYear = function (birtDate) {
  const birthYear = birtDate.getFullYear()
  return birthYear + WORK_START_AGE
}

export {
  delay,
  calculateMinimumAmortizedLoanPayment,
  calculateMinimumRevolvingLoanPayment,
  asDollar,
  debounce,
  mandatoryFieldRule,
  copyToClipboard,
  makeSeoHeaders,
  estimateMaxRrspContributionLimit,
  estimateMaxTfsaContributionLimit,
  estimateWorkStartYear
}
