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
  const discountFactor = ((1 + monthlyInterestRate) ** months - 1) / monthlyInterestRate * (1 + monthlyInterestRate) ** months
  return Math.round(principal / discountFactor)
}

const calculateMinimumRevolvingLoanPayment = function (principal, apr) {
  return principal * apr / 12
}

const asDollar = function (num) {
  return num.toLocaleString('en-CA', { style: 'currency', currency: 'CAD', minimumFractionDigits: 0 })
}

export { delay, calculateMinimumAmortizedLoanPayment, calculateMinimumRevolvingLoanPayment, asDollar }
