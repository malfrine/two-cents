<template>
  <v-container fluid>
    <v-stepper v-model="currentStep" style="min-height: 86vh; background: #121212">
      <v-stepper-items>
        <v-stepper-content step="1" :class="isSmallView ? 'pa-0 ma-0': ''">
          <BaseQuestion
            question="Are you saving up for a big purchase?"
            information="This could be a down payment on a house, a wedding, your child's education, etc."
            @continue="isSavingUpForBigPurchase ? goToNext() : goTo(3)"
            @back="goBack"
          >
            <v-radio-group v-model="bigPurchaseSelection" class="mb-2 mt-n1">
              <v-radio
                v-for="(description, index) in bigPurchaseOptions"
                :key="index"
                :label="description"
                :value="description"
              />
            </v-radio-group>
          </BaseQuestion>
        </v-stepper-content>
        <v-stepper-content step="2" :class="isSmallView ? 'pa-0 ma-0': ''">
          <BaseQuestion
            question="Tell us about your next big purchase"
            @continue="goToNextIfValidForm('big-purchase')"
            @back="goBack"
          >
            <v-form ref="big-purchase">
              <v-text-field
                v-model="nextBigPurchaseAmount"
                label="Amount to Save"
                outlined
                :rules="[mandatoryField('Amount to save'), nonNegativeNumberRule('Your next purchase')]"
                type="number"
              />
              <v-text-field
                v-model="nextBigPurchaseDate"
                label="Expected Purchase Date"
                outlined
                type="date"
                :rules="[mandatoryField('Expected purchase date'), v => new Date(v) > new Date() || `Purchase date must be in the future` ]"
              />
            </v-form>
          </BaseQuestion>
        </v-stepper-content>
        <v-stepper-content step="3" :class="isSmallView ? 'pa-0 ma-0': ''">
          <BaseQuestion
            question="What is your ideal retirement age?"
            @continue="goToNextIfValidForm('retirement-age')"
            @back="goBack"
          >
            <v-form ref="retirement-age">
              <v-text-field
                v-model="retirementAge"
                outlined
                :rules="[mandatoryField('Retirement age'), nonNegativeNumberRule('Your retirement age')]"
                type="number"
              />
            </v-form>
          </BaseQuestion>
        </v-stepper-content>
        <v-stepper-content step="4" :class="isSmallView ? 'pa-0 ma-0': ''">
          <BaseQuestion
            question="Do you have a nest egg fund?"
            information="Most experts recommend having 3-6 months of your living expenses in your rainy day fund."
            @continue="isRainyDayFundValueRequired ? goToNext() : goTo(6)"
            @back="goBack"
          >
            <v-radio-group v-model="rainyDayFundSelection" class="mb-2 mt-n1">
              <v-radio
                v-for="(description, index) in rainyDayFundOptions"
                :key="index"
                :label="description"
                :value="description"
              />
            </v-radio-group>
          </BaseQuestion>
        </v-stepper-content>
        <v-stepper-content step="5" :class="isSmallView ? 'pa-0 ma-0': ''">
          <BaseQuestion
            question="How much do you have saved up in your nest egg fund?"
            @continue="goToNextIfValidForm('nest-egg')"
            @back="goBack"
          >
            <v-form ref="nest-egg">
              <v-text-field
                v-model="currentNestEggFundAmount"
                label="Amount Saved"
                outlined
                :rules="[mandatoryField('Amount Saved'), nonNegativeNumberRule('Your nest egg amount')]"
                type="number"
              />
            </v-form>
          </BaseQuestion>
        </v-stepper-content>
        <v-stepper-content step="6" :class="isSmallView ? 'pa-0 ma-0': ''">
          <BaseQuestion
            question="What's your name?"
            @continue="goToNextIfValidForm('name')"
            @back="goBack"
          >
            <v-form ref="name">
              <v-text-field
                v-model="firstName"
                outlined
                :rules="[mandatoryField('Your name')]"
              />
            </v-form>
          </BaseQuestion>
        </v-stepper-content>
        <v-stepper-content step="7" :class="isSmallView ? 'pa-0 ma-0': ''">
          <BaseQuestion
            question="When were you born?"
            @continue="goToNextIfValidForm('birth_date')"
            @back="goBack"
          >
            <v-form ref="birth_date">
              <v-text-field
                v-model="birthDate"
                outlined
                :rules="[mandatoryField('Your birth date'), v => new Date(v) < new Date() || 'You must be born in the past']"
                type="date"
              />
            </v-form>
          </BaseQuestion>
        </v-stepper-content>
        <v-stepper-content step="8" :class="isSmallView ? 'pa-0 ma-0': ''">
          <BaseQuestion
            question="What province do you live in?"
            information="This helps us calculate your income tax"
            @continue="goToNextIfValidForm('province')"
            @back="goBack"
          >
            <v-form ref="province">
              <v-autocomplete
                v-model="province"
                outlined
                :items="$constants.provinces"
                :rules="[mandatoryField('Your province')]"
              />
            </v-form>
          </BaseQuestion>
        </v-stepper-content>
        <v-stepper-content step="9" :class="isSmallView ? 'pa-0 ma-0': ''">
          <BaseQuestion
            question="What is your monthly income before taxes?"
            @continue="goToNextIfValidForm('income')"
            @back="goBack"
          >
            <v-form ref="income">
              <v-text-field
                v-model="preTaxMonthlyIncome"
                outlined
                prefix="$"
                :rules="[mandatoryField('Your income'), nonNegativeNumberRule('Your income')]"
                type="number"
              />
            </v-form>
          </BaseQuestion>
        </v-stepper-content>
        <v-stepper-content step="10" :class="isSmallView ? 'pa-0 ma-0': ''">
          <BaseQuestion
            question="What percent of your income goes towards long-term goals?"
            information="This includes paying off loans (including mortgages), investing, saving for a rain day, etc."
            @continue="goToNextIfValidForm('savings-percentage'); setDefaultContributionLimits()"
            @back="goBack"
          >
            <v-form ref="savings-percentage">
              <v-text-field
                v-model="savingsPercentage"
                outlined
                suffix="%"
                :rules="[mandatoryField('Savings percentage'), nonNegativeNumberRule('The number'), v => v <= 100 || 'The number must be less than 100']"
                type="number"
              />
            </v-form>
          </BaseQuestion>
        </v-stepper-content>
        <v-stepper-content step="11" :class="isSmallView ? 'pa-0 ma-0': ''">
          <BaseQuestion
            question="Which of the following statements best describes your risk tolerance"
            @continue="goToNext"
            @back="goBack"
          >
            <v-radio-group v-model="riskToleranceDescription" class="mb-2 mt-n1">
              <v-radio
                v-for="(description, index) in riskToleranceItems"
                :key="index"
                :label="description"
                :value="description"
              />
            </v-radio-group>
          </BaseQuestion>
        </v-stepper-content>
        <v-stepper-content step="12" :class="isSmallView ? 'pa-0 ma-0': ''">
          <BaseQuestion
            question="What are your contribution limits?"
            information="<p>You can find this information by logging in to your <a href='https://www.canada.ca/en/revenue-agency/services/e-services/cra-login-services.html' target='_blank'>CRA account</a> or by checking your most recent Notice of Assessment from the CRA.</p> <p>We have provided some estimates assuming you haven't made any contributions before.</p>"
            @continue="goToNextIfValidForm('registered-contributions')"
            @back="goBack"
          >
            <v-form ref="registered-contributions">
              <v-text-field
                v-model="tfsaContributionLimit"
                label="TFSA Contribution Limit"
                outlined
                prefix="$"
                :rules="[mandatoryField('TFSA contribution limit'), nonNegativeNumberRule('Your TFSA contribution limit')]"
                type="number"
              />
              <v-text-field
                v-model="rrspContributionLimit"
                label="RRSP Contribution Limit"
                outlined
                prefix="$"
                :rules="[mandatoryField('RRSP contribution limit'), nonNegativeNumberRule('Your RRSP contribution limit')]"
                type="number"
              />
            </v-form>
          </BaseQuestion>
        </v-stepper-content>
        <v-stepper-content step="13" :class="isSmallView ? 'pa-0 ma-0': ''">
          <BaseQuestion
            question="How much money do you have in your investment accounts?"
            @continue="goToNextIfValidForm('investments')"
            @back="goBack"
          >
            <v-form ref="investments">
              <v-text-field
                v-model="tfsaInvestmentCurrentBalance"
                label="TFSA"
                outlined
                prefix="$"
                :rules="[mandatoryField('TFSA investment amount'), nonNegativeNumberRule('Your TFSA investment amount')]"
                type="number"
              />
              <v-text-field
                v-model="rrspInvestmentCurrentBalance"
                label="RRSP"
                outlined
                prefix="$"
                :rules="[mandatoryField('RRSP investment amount'), nonNegativeNumberRule('Your RRSP investment amount')]"
                type="number"
              />
              <v-text-field
                v-model="nonRegisteredInvestmentCurrentBalance"
                label="Other Accounts"
                outlined
                prefix="$"
                :rules="[mandatoryField('Non-registered account investment amount'), nonNegativeNumberRule('Your non-registered investment amount')]"
                type="number"
              />
            </v-form>
          </BaseQuestion>
        </v-stepper-content>
        <v-stepper-content step="14" :class="isSmallView ? 'pa-0 ma-0': ''">
          <BaseQuestion
            question="Select all the loans that you currently have"
            @continue="goToNext()"
            @back="goBack"
          >
            <v-checkbox
              v-for="(loan, index) in loanOptions"
              :key="index"
              v-model="loans"
              class="my-n3"
              :label="loan"
              :value="loan"
            />
          </BaseQuestion>
        </v-stepper-content>
        <v-stepper-content
          v-for="(loanName, index) in loans"
          :key="index"
          :step="index + 15"
          :class="isSmallView ? 'pa-0 ma-0': ''"
        >
          <BaseQuestion
            :question="loanObject[loanName].question"
            :information="loanObject[loanName].information"
            @continue="goToNextIfValidForm(loanName)"
            @back="goBack"
          >
            <v-form :ref="loanName">
              <v-text-field
                v-model="loanObject[loanName].balance"
                :label="`${loanName} Current Balance`"
                prefix="$"
                outlined
                :rules="[mandatoryField(`${loanObject[loanName].mandatoryFieldText} current balance`), nonNegativeNumberRule(`Your ${loanObject[loanName].mandatoryFieldText} current balance`)]"
                type="number"
              />
              <v-text-field
                v-if="loanObject[loanName].needsDueDate"
                v-model="loanObject[loanName].date"
                :label="`${loanName} End Date`"
                outlined
                type="date"
                :rules="[mandatoryField(`${loanObject[loanName].mandatoryFieldText} due date`)]"
              />
            </v-form>
          </BaseQuestion>
        </v-stepper-content>
        <v-stepper-content :step="numLoans + 15">
          <BaseQuestion
            question="Register your email and password"
            @continue="validateForm('register'); onboardUser()"
            @back="goBack"
          >
            <v-form ref="register">
              <v-text-field
                v-model="email"
                label="Email"
                outlined
                type="email"
                :rules="[mandatoryField('Email'), emailRule()]"
              />
              <v-text-field
                v-model.trim="password"
                label="Password"
                outlined
                type="password"
                :rules="[mandatoryField('Password'), v => v.length >= 8 || 'Password must have at least 8 characters']"
              />
              <v-text-field
                v-model.trim="confirmPassword"
                label="Confirm Password"
                outlined
                type="password"
                :rules="[mandatoryField('Password')]"
              />
              <div class="text-caption">
                <p class="mt-n3">
                  <em>Note that you can only join if you are an approved beta tester. Please join our <a href="/waitlist/join">waitlist</a> if you are not on it already! </em>
                </p>
              </div>
            </v-form>
          </BaseQuestion>
        </v-stepper-content>
      </v-stepper-items>
    </v-stepper>
  </v-container>
</template>

<script>
import BaseQuestion from '@/components/onboarding/BaseQuestion.vue'
import { mandatoryField, nonNegativeNumberRule, emailRule } from '~/assets/rules.js'
import {
  makeSeoHeaders,
  estimateMaxRrspContributionLimit,
  estimateMaxTfsaContributionLimit,
  estimateWorkStartYear
} from '~/assets/utils.js'

export default {
  layout: 'simple',
  components: {
    BaseQuestion
  },
  data () {
    return {
      currentStep: 1,
      stepPath: [],
      riskToleranceObject: {
        'Play it safe always': 0,
        'Some risk never hurt anyone': 25,
        'Medium risk': 50,
        'High risk, high reward': 75,
        'Stonks only go up!': 100
      },
      bigPurchaseObject: {
        "Yes, I'm saving up for something big!": true,
        'Not right now': false
      },
      rainDayFundObject: {
        'Yes, I have enough to last me 6 months': false,
        'Yes, but not enough to last me 6 months': true,
        'Not yet!': true
      },
      loanObject: {
        Mortgage: {
          question: 'Tell us about your mortgage',
          mandatoryFieldText: 'Mortgage',
          needsDueDate: true
        },
        'Student Loan': {
          question: 'Tell us about your student loans',
          mandatoryFieldText: 'Student loan',
          needsDueDate: true
        },
        'Credit Card': {
          question: 'Tell us about your credit card loans',
          mandatoryFieldText: 'Credit card loan',
          needsDueDate: false
        },
        'Personal Loan': {
          question: 'Tell us about your personal loans',
          mandatoryFieldText: 'Personal loan',
          needsDueDate: true
        },
        'Line of Credit': {
          question: 'Tell us about your line of credit',
          mandatoryFieldText: 'Line of credit',
          needDueDate: false
        },
        'Student Line of Credit': {
          question: 'Tell us about your student line of credit',
          mandatoryFieldText: 'Student line of credit',
          needsDueDate: false
        },
        'Car Loan': {
          question: 'Tell us about your car loan',
          mandatoryFieldText: 'Car loan',
          needsDueDate: true
        }
      },
      // user onboarding data
      bigPurchaseSelection: "Yes, I'm saving up for something big!",
      nextBigPurchaseAmount: null,
      nextBigPurchaseDate: null,
      rainyDayFundSelection: 'Not yet!',
      retirementAge: 60,
      currentNestEggFundAmount: null,
      firstName: null,
      birthDate: null,
      province: null,
      preTaxMonthlyIncome: null,
      savingsPercentage: 20,
      riskToleranceDescription: 'Medium risk',
      tfsaContributionLimit: null,
      rrspContributionLimit: null,
      tfsaInvestmentCurrentBalance: null,
      rrspInvestmentCurrentBalance: null,
      nonRegisteredInvestmentCurrentBalance: null,
      loans: [],
      email: null,
      password: '',
      confirmPassword: ''
    }
  },
  computed: {
    isSmallView () {
      return this.$vuetify.breakpoint.xs
    },
    riskToleranceItems () {
      return Object.keys(this.riskToleranceObject)
    },
    bigPurchaseOptions () {
      return Object.keys(this.bigPurchaseObject)
    },
    isSavingUpForBigPurchase () {
      return this.bigPurchaseObject[this.bigPurchaseSelection]
    },
    isRainyDayFundValueRequired () {
      return this.rainDayFundObject[this.rainyDayFundSelection]
    },
    rainyDayFundOptions () {
      return Object.keys(this.rainDayFundObject)
    },
    loanOptions () {
      return Object.keys(this.loanObject)
    },
    numLoans () {
      return this.loans.length
    }
  },
  methods: {
    mandatoryField,
    nonNegativeNumberRule,
    emailRule,
    setDefaultContributionLimits () {
      if (!this.birthDate || !this.preTaxMonthlyIncome) {
        return
      }
      const birthDate = new Date(this.birthDate)
      const avgAnnualIncome = 0.9 * 12 * Number(this.preTaxMonthlyIncome)
      if (!this.tfsaContributionLimit) {
        this.tfsaContributionLimit = estimateMaxTfsaContributionLimit(birthDate.getFullYear())
      }
      if (!this.rrspContributionLimit) {
        const workStartYear = estimateWorkStartYear(birthDate)
        this.rrspContributionLimit = estimateMaxRrspContributionLimit(workStartYear, avgAnnualIncome)
      }
    },
    goBack () {
      const backStep = this.stepPath.pop()
      if (backStep) {
        this.currentStep = backStep
      } else {
        this.$router.go(-1)
      }
    },
    goTo (nextStep) {
      this.stepPath.push(this.currentStep)
      this.currentStep = nextStep
    },
    goToNext () {
      this.goTo(this.currentStep + 1)
    },
    validateForm (formName) {
      let form = this.$refs[formName]
      if (Array.isArray(form)) {
        form = form[0]
      }
      return form.validate()
    },
    goToNextIfValidForm (formName) {
      if (this.validateForm(formName)) {
        this.goToNext()
      }
    },
    onboardUser () {
      if (!this.validateForm('register')) {
        return
      }

      const userInfo = {}
      const riskTolerance = this.riskToleranceObject[this.riskToleranceDescription]
      // add account info
      if (this.password !== this.confirmPassword) {
        this.$toast.error('Passwords do not match')
        return
      }
      userInfo.account = {
        email: this.email,
        password: this.password,
        first_name: this.firstName || 'hi'
      }
      // add basic info
      userInfo.financial_profile = {
        birth_date: this.birthDate,
        retirement_age: this.retirementAge,
        risk_tolerance: riskTolerance,
        monthly_salary_before_tax: this.preTaxMonthlyIncome,
        percent_salary_for_spending: this.savingsPercentage,
        starting_rrsp_contribution_limit: this.rrspContributionLimit,
        starting_tfsa_contribution_limit: this.tfsaContributionLimit,
        province_of_residence: this.province
      }
      // add goals
      userInfo.goals = {}
      if (this.isSavingUpForBigPurchase) {
        userInfo.goals.big_purchase = {
          amount: this.nextBigPurchaseAmount,
          date: this.nextBigPurchaseDate
        }
      }
      if (this.isRainyDayFundValueRequired) {
        userInfo.goals.current_nest_egg_amount = this.currentNestEggFundAmount || 0
      }
      // add investments
      userInfo.investments = {
        tfsa: this.tfsaInvestmentCurrentBalance || 0,
        rrsp: this.rrspInvestmentCurrentBalance || 0,
        non_registered: this.nonRegisteredInvestmentCurrentBalance || 0
      }
      // add loans
      userInfo.loans = {}
      for (const loan of this.loans) {
        userInfo.loans[loan] = {
          balance: this.loanObject[loan].balance || 0,
          date: this.loanObject[loan].date
        }
      }

      console.log(userInfo)

      this.$axios.post(
        '/api/my/account/onboard', userInfo
      )
        .then(
          () => {
            this.$fire.auth.signOut() // just in case they were signed in as someone else
            this.$router.push('login')
          }
        )
        .catch((e) => {
          this.$toast.error('Sorry, could not register your account')
        })
    }
  },
  head () {
    const title = 'Get started planning your finances today!'
    return {
      title: 'Build your plan',
      meta: makeSeoHeaders(title)
    }
  }
}
</script>
