const mandatoryField = function (fieldName) {
  return v => !!v || `${fieldName} is required`
}

const emailRule = function () {
  return v => /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(v) || 'E-mail must be valid'
}

const emailRules = [
  mandatoryField('Email'),
  emailRule
]

const nonNegativeNumberRule = function (fieldName) {
  return v => v >= 0 || `${fieldName} cannot be less than 0`
}

export { emailRules, emailRule, mandatoryField, nonNegativeNumberRule }
