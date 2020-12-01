<template>
  <div class="col-12 col-sm-6 col-lg-4 col-xl-3 pb-2">
    <div class="card shadow" align="center">
      <div align="left">
        <div class="card-header">
          <div class="row justify-content-end">
            <div
              class="btn btn-sm mt--3"
              id="edit-delete-dropdown"
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
                v-on:click.prevent="deleteLoan(loan)"
                href=""
                >Delete</button
              >
              <div class="dropdown-divider"></div>
              <button
                type="button"
                class="dropdown-item"
                data-toggle="modal"
                v-bind:data-target="'#editLoanModal' + loan.id"
              >
                Edit
              </button>
            </div>
          </div>
          <div align="left"> {{ loan.name }}</div>
          <h5 class="display-3 card-title text-primary mb--2">$ {{ loan.currentBalance }}</h5>
          <div class="row justify-content-center">
          <div
            class="btn btn-sm mb--3"
            type="button"
            data-toggle="collapse"
            v-bind:data-target="'#collapse-target' + loan.id"
            aria-expanded="false"
            aria-controls="collapse-target"
            align="center"
            v-on:click.prevent="changeShowMode()"
          >
            <font-awesome-icon v-if="!this.showAllInfo" icon="caret-down"></font-awesome-icon>
            <font-awesome-icon v-else icon="caret-up"></font-awesome-icon>
          </div>
          </div>
        </div>
        <div class="collapse" v-bind:id="'collapse-target' + loan.id">
          <div class="card-body">
            <p class="card-text small mt--3">{{ loan.apr }}% <em>APR</em></p>
            <p class="card-text small mt--3"><em>Minimum Payment:</em> ${{ loan.minimumMonthlyPayment }}</p>
            <p class="card-text small mt--3"><em>Due:</em> {{ loan.dueDate }}</p>
          </div>
        </div>
      </div>
    </div>
    <loan-modal
      v-bind:modalName="'editLoanModal' + loan.id"
      v-bind:loanId="loan.id"
    >
    </loan-modal>
  </div>
</template>

<script>
import LoanModal from './LoanModal.vue'
import { mapActions } from 'vuex'

export default {
  components: {
    LoanModal
  },
  data () {
    return {
      showAllInfo: false
    }
  },
  props: ['loanId'],
  methods: {
    changeShowMode () { this.showAllInfo = !this.showAllInfo },
    ...mapActions('instruments', ['deleteLoan'])
  },
  computed: {
    loan () { return this.$store.getters['instruments/getLoanById'](this.loanId) }
  }
}
</script>
