<template>
  <div>
    <v-row class="mb-4 ml-1">
      <v-btn
        fab
        large
        color="accent"
        @click.stop="showInvestmentDialog=true"
      >
        <v-icon>mdi-plus</v-icon>
      </v-btn>
    </v-row>
    <v-row justify="center" justify-lg="start">
      <investment-card
        v-for="investment in investments"
        :key="investment.id"
        :investment-id="investment.id"
      />
    </v-row>
    <InvestmentDialog :visible="showInvestmentDialog" :investment-id="null" @close="showInvestmentDialog=false" />
  </div>
</template>

<script>
import InvestmentCard from '@/components/finances/InvestmentCard.vue'
import InvestmentDialog from '@/components/finances/InvestmentDialog.vue'

export default {
  components: { InvestmentCard, InvestmentDialog },
  data () {
    return {
      showInvestmentDialog: false
    }
  },
  computed: {
    investments () {
      return this.$store.getters['finances/getInvestments']
    }
  }
}
</script>
