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
                href=""
                @click.prevent="deleteLoan(loan)"
              >
                Delete
              </button>
              <div class="dropdown-divider" />
              <button
                type="button"
                class="dropdown-item"
                data-toggle="modal"
                :data-target="'#editLoanModal' + loan.id"
              >
                Edit
              </button>
            </div>
          </div>
          <div align="left">
            {{ loan.name }}
          </div>
          <h5 class="display-3 card-title text-primary mb--2">
            $ {{ loan.current_balance }}
          </h5>
          <div class="row justify-content-center">
            <div
              class="btn btn-sm mb--3"
              type="button"
              data-toggle="collapse"
              :data-target="'#collapse-target' + loan.id"
              aria-expanded="false"
              aria-controls="collapse-target"
              align="center"
              @click.prevent="changeShowMode()"
            >
              <v-icon v-if="!this.showAllInfo">
                mdi-chevron-down
              </v-icon>
              <v-icon v-else>
                mdi-chevron-up
              </v-icon>
            </div>
          </div>
        </div>
        <div :id="'collapse-target' + loan.id" class="collapse">
          <div class="card-body">
            <p class="card-text small mt--3">
              {{ loan.apr }}% <em>APR</em>
            </p>
            <p class="card-text small mt--3">
              <em>Minimum Payment:</em> ${{ loan.minimum_monthly_payment }}
            </p>
            <p class="card-text small mt--3">
              <em>Due:</em> {{ loan.end_date }}
            </p>
          </div>
        </div>
      </div>
    </div>
    <loan-modal
      :modal-name="'editLoanModal' + loan.id"
      :loan-id="loan.id"
    />
  </div>
</template>

<script>
import { mapActions } from 'vuex'
import LoanModal from './LoanModal.vue'

export default {
  components: {
    LoanModal
  },
  props: ['loanId'],
  data () {
    return {
      showAllInfo: false
    }
  },
  methods: {
    changeShowMode () { this.showAllInfo = !this.showAllInfo },
    ...mapActions('finances', ['deleteLoan'])
  },
  computed: {
    loan () {
      return this.$store.getters['finances/getLoanById'](this.loanId)
    }
  }
}
</script>
