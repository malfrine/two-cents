<template>
  <!-- Modal -->
  <div>
    <div
      class="modal fade"
      v-bind:id="modalName"
      tabindex="-1"
      role="dialog"
      aria-labelledby="modalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h2 class="modal-title text-primary">
              Tell us about your investment
            </h2>
            <button
              type="button"
              class="close"
              data-dismiss="modal"
              aria-label="Close"
            >
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <form>
              <div class="form-group">
                <label class="form-control-label" for="name"
                  >Investment Name</label
                >
                <input
                  type="text"
                  class="form-control pl-2"
                  v-model.lazy="investment.name"
                  placeholder="Your Investment Name"
                />
              </div>
              <div class="form-group">
                <label class="form-control-label" for="current-balance"
                  >Current Balance</label
                >
                <div class="input-group">
                  <div class="input-group-prepend">
                    <span class="input-group-text bg-light" id="basic-addon1"
                      >$</span
                    >
                  </div>
                  <input
                    type="number"
                    class="form-control pl-2"
                    v-model.lazy="investment.current_balance"
                    placeholder="10000"
                  />
                </div>
              </div>
              <div class="form-group">
                <label class="form-control-label" for="risk_level">Risk Level</label>
                <div class="input-group">
                  <input
                    type="string"
                    class="form-control pl-2 pr-2"
                    v-model.lazy="investment.risk_level"
                    placeholder="Medium"
                  />
                </div>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-primary"
              data-dismiss="modal"
              @click="createOrUpdateInvestment()"
            >
              Save Investment
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// import { mapActions } from 'vuex'

export default {
  props: ['modalName', 'investmentId'],
  methods: {
    createOrUpdateInvestment () {
      this.$store.dispatch('finances/createOrUpdateInvestment', this.investment)
    }
  },
  computed: {
    investment () {
      const investment = this.$store.getters['finances/getInvestmentById'](this.investmentId)
      if (investment === null) {
        return {
          name: null,
          current_balance: null,
          risk_level: null
        }
      } else {
        return { ...investment }
      }
    }

  }
}
</script>
