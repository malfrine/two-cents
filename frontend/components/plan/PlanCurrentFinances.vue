<template>
  <v-row>
    <v-col cols="12" md="6">
      <v-card class="pb-1" style="min-height: 100px">
        <v-card-title>
          {{ possessiveUserName }} Loans
        </v-card-title>
        <v-divider class="mt-n2 mb-3" />
        <div v-if="userHasLoans" class="py-1">
          <v-row v-for="loan in loans" :key="loan.id" class="px-6 my-2">
            <div class="text">
              {{ loan.name }}
            </div>
            <v-spacer />
            <div class="text red--text">
              $ {{ loan.current_balance }}
            </div>
          </v-row>
          <v-divider />
          <v-row class="px-6 my-2">
            <div class="text">
              Total Loans
            </div>
            <v-spacer class="my-2" />
            <div class="text red--text">
              $ {{ totalLoans }}
            </div>
          </v-row>
        </div>
        <div v-else>
          <v-container fluid>
            <div class="h3-text">
              No loans added
            </div>
          </v-container>
        </div>
      </v-card>
    </v-col>
    <v-col cols="12" md="6">
      <v-card class="pb-1">
        <v-card-title>
          {{ possessiveUserName }} Investments
        </v-card-title>
        <v-divider class="mt-n2 mb-3" />
        <div v-if="userHasInvestments" class="py-1">
          <v-row v-for="inv in investments" :key="inv.id" class="px-6 my-2">
            <div class="text">
              {{ inv.name }}
            </div>
            <v-spacer />
            <div class="text primary--text">
              $ {{ inv.current_balance }}
            </div>
          </v-row>
          <v-divider />
          <v-row class="px-6 my-2">
            <div class="text">
              Total Investments
            </div>
            <v-spacer class="my-2" />
            <div class="text primary--text">
              $ {{ totalInvestments }}
            </div>
          </v-row>
        </div>
        <div v-else>
          <v-container fluid>
            <div class="h2-text">
              No investments added
            </div>
          </v-container>
        </div>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
export default {
  computed: {
    userHasLoans () {
      return (Object.keys(this.loans)).length > 0
    },
    loans () {
      return this.$store.getters['finances/getLoans']
    },
    userHasInvestments () {
      return (Object.keys(this.investments)).length > 0
    },
    investments () {
      return this.$store.getters['finances/getInvestments']
    },
    totalInvestments () {
      let total = 0
      for (const id in this.investments) {
        total += this.investments[id].current_balance
      }
      return total
    },
    totalLoans () {
      let total = 0
      for (const id in this.loans) {
        total += this.loans[id].current_balance
      }
      return total
    },
    possessiveUserName () {
      const firstName = this.$store.getters['finances/getFirstName']
      const posession = firstName.slice(-1) === 's' ? "'" : "'s"
      return `${firstName}${posession}`
    }
  }
}
</script>
