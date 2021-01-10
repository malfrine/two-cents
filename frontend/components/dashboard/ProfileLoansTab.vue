<template>
  <div>
    <v-row class="mb-4 ml-1">
      <v-btn
        fab
        large
        color="primary"
        @click.stop="showLoanDialog=true"
      >
        <v-icon>mdi-plus</v-icon>
      </v-btn>
    </v-row>
    <v-row justify="center" justify-lg="start">
      <loan-card
        v-for="loan in loans"
        :key="loan.id"
        :loan-id="loan.id"
      />
    </v-row>
    <LoanDialog :visible="showLoanDialog" :loan-id="null" @close="showLoanDialog=false" />
  </div>
</template>

<script>
import LoanCard from '@/components/finances/LoanCard.vue'
import LoanDialog from '@/components/finances/LoanDialog.vue'

export default {
  components: { LoanCard, LoanDialog },
  data () {
    return {
      showLoanDialog: false
    }
  },
  computed: {
    loans () {
      return this.$store.getters['finances/getLoans']
    }
  }
}
</script>
