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

export {
  delay,
  calculateMinimumAmortizedLoanPayment,
  calculateMinimumRevolvingLoanPayment,
  asDollar,
  debounce,
  mandatoryFieldRule,
  copyToClipboard
}
