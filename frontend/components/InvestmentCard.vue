<template>
  <div class="col-12 col-sm-6 col-lg-4 col-xl-3 pb-2">
    <div class="card shadow" align="center">
      <div align="left">
        <div class="card-header">
          <div class="row justify-content-end">
            <div
              id="edit-delete-dropdown"
              class="btn btn-sm mt--3"
              type="button"
              data-toggle="dropdown"
              aria-haspopup="true"
              aria-expanded="false"
            >
              ...
            </div>
            <div
              class="dropdown-menu"
              aria-labelledby="edit-delete-dropdown"
              align="center"
            >
              <button
                class="dropdown-item"
                @click.prevent="deleteInvestment(investment)"
              >
                Delete
              </button>
              <div class="dropdown-divider" />
              <button
                type="button"
                class="dropdown-item"
                data-toggle="modal"
                :data-target="'#editInvestmentModal' + investment.id"
              >
                Edit
              </button>
            </div>
          </div>
          <div align="left">
            {{ investment.name }}
          </div>
          <h5 class="display-3 card-title text-primary mb--2">
            $ {{ investment.current_balance }}
          </h5>
          <div class="row justify-content-center">
            <div
              class="btn btn-sm mb--3"
              type="button"
              data-toggle="collapse"
              :data-target="'#collapse-target-investment' + investment.id"
              aria-expanded="false"
              aria-controls="collapse-target"
              align="center"
              @click.prevent="changeShowMode()"
            >
              <v-icon v-if="!showAllInfo">
                mdi-chevron-down
              </v-icon>
              <v-icon v-else>
                mdi-chevron-up
              </v-icon>
            </div>
          </div>
        </div>
        <div
          :id="'collapse-target-investment' + investment.id"
          class="collapse"
        >
          <div class="card-body">
            <p class="card-text small mt--3">
              <em>Risk Level:</em> {{ investment.risk_level }}
            </p>
          </div>
        </div>
      </div>
    </div>
    <investment-modal
      :modal-name="'editInvestmentModal' + investment.id"
      :investment-id="investment.id"
    />
  </div>
</template>

<script>
import { mapActions } from 'vuex'
import InvestmentModal from './InvestmentModal.vue'

export default {
  components: {
    InvestmentModal
  },
  props: ['investmentId'],
  data () {
    return {
      showAllInfo: false
    }
  },
  methods: {
    changeShowMode () {
      this.showAllInfo = !this.showAllInfo
    },
    ...mapActions('finances', ['deleteInvestment'])
  },
  computed: {
    investment () {
      return this.$store.getters['finances/getInvestmentById'](
        this.investmentId
      )
    }
  }
}
</script>
