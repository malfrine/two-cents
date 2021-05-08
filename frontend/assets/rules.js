const mandatoryField = function (fieldName) {
  return v => !!v || `${fieldName} is required`
}

const emailRules = [
  mandatoryField('Email'),
  v => /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(v) || 'E-mail must be valid'
]

export { emailRules }
