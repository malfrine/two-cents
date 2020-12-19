<template>
  <!-- Modal -->
  <div>
    <div
      class="modal fade"
      v-bind:id="modalName"
      tabindex="-1"
      role="dialog"
      aria-labelledby="exampleModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h2 class="modal-title text-primary">Tell us about your loan  </h2>
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
                <label class="form-control-label" for="name">Loan Name</label>
                <input
                  type="text"
                  class="form-control pl-2"
                  v-model.lazy="localLoan.name"
                  placeholder="Your Loan Name"
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
                    v-model.lazy="localLoan.current_balance"
                    placeholder=10000
                  />
                </div>
              </div>
              <div class="form-group">
                <label class="form-control-label" for="apr">APR</label>
                <div class="input-group">
                  <input
                    type="number"
                    class="form-control pl-2 pr-2"
                    v-model.lazy="localLoan.apr"
                    placeholder="5"
                  />
                  <div class="input-group-append">
                    <span
                      class="input-group-text bg-light"
                      id="apr-percent-addon"
                      >%</span
                    >
                  </div>
                </div>
              </div>
              <div class="form-group">
                <label class="form-control-label" for="min-monthly-payment"
                  >Minimum Monthly Payment</label
                >
                <div class="input-group">
                  <div class="input-group-prepend">
                    <span class="input-group-text bg-light" id="basic-addon1"
                      >$</span
                    >
                  </div>
                  <input
                    type="number"
                    class="form-control pl-2 pr-2"
                    v-model.lazy="localLoan.minimum_monthly_payment"
                    placeholder="5"
                  />
                </div>
              </div>
              <div class="form-group">
                <label class="form-control-label" for="due-date"
                  >Due Date</label
                >
                <input
                  type="date"
                  class="form-control pl-2 pr-2"
                  v-model.lazy="localLoan.end_date"
                />
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-primary"
              data-dismiss="modal"
              @click="createOrUpdateLoan()"
            >
              Save Loan
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
  props: ['modalName', 'loanId'],
  methods: {
    createOrUpdateLoan () {
      this.$store.dispatch('finances/createOrUpdateLoan', this.localLoan)
    }
  },
  computed: {
    localLoan () {
      const loan = this.$store.getters['finances/getLoanById'](this.loanId)
      if (loan === null) {
        return {
          name: null,
          current_balance: null,
          apr: null,
          minimum_monthly_payment: null,
          end_date: null,
          id: null
        }
      } else {
        return { ...loan }
      }
    }
  }
}
</script>
