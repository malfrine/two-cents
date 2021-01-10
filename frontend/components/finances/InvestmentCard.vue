<template>
  <base-instrument-card>
    <template v-slot:fixed>
      <v-row class="mx-3">
        <v-card-subtitle class="mb-n7">
          <div class="text-h6">
            {{ investment.name }}
          </div>
        </v-card-subtitle>
        <v-spacer />
        <v-speed-dial
          v-model="fab"
          direction="bottom"
          class="mt-2"
        >
          <template v-slot:activator>
            <v-btn
              v-model="fab"
              icon
              fab
              small
            >
              <v-icon v-if="fab">
                mdi-close
              </v-icon>
              <v-icon v-else>
                mdi-dots-horizontal
              </v-icon>
            </v-btn>
          </template>
          <v-btn
            fab
            small
            color="blue"
            @click.stop="showInvestmentDialog=true"
          >
            <v-icon>mdi-pencil</v-icon>
          </v-btn>
          <v-btn
            fab
            small
            color="red"
            @click.prevent="deleteInvestment(investment)"
          >
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </v-speed-dial>

        <InvestmentDialog :visible="showInvestmentDialog" :investment-id="investment.id" @close="showInvestmentDialog=false" />
      </v-row>
      <v-card-title>
        <div class="text-h2 primary--text" color="primary">
          $ {{ investment.current_balance }}
        </div>
      </v-card-title>
    </template>
    <template v-slot:hidden>
      <v-card-text>
        <p class="mt-n5">
          <em>Risk Level:</em> {{ investment.risk_level }}
        </p>
      </v-card-text>
    </template>
  </base-instrument-card>
</template>

<script>
import { mapActions } from 'vuex'
import InvestmentDialog from '@/components/finances/InvestmentDialog.vue'

export default {
  components: {
    InvestmentDialog
  },
  props: ['investmentId'],
  data () {
    return {
      showInvestmentDialog: false,
      showAllInfo: false,
      fab: false
    }
  },

  methods: {
    ...mapActions('finances', ['deleteInvestment'])
  },
  computed: {
    investment () {
      return this.$store.getters['finances/getInvestmentById'](this.investmentId)
    }
  }
}
</script>
