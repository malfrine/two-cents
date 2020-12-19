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
                v-on:click.prevent="deleteInvestment(investment)"
              >
                Delete
              </button>
              <div class="dropdown-divider"></div>
              <button
                type="button"
                class="dropdown-item"
                data-toggle="modal"
                v-bind:data-target="'#editInvestmentModal' + investment.id"
              >
                Edit
              </button>
            </div>
          </div>
          <div align="left">{{ investment.name }}</div>
          <h5 class="display-3 card-title text-primary mb--2">
            $ {{ investment.current_balance }}
          </h5>
          <div class="row justify-content-center">
            <div
              class="btn btn-sm mb--3"
              type="button"
              data-toggle="collapse"
              v-bind:data-target="'#collapse-target-investment' + investment.id"
              aria-expanded="false"
              aria-controls="collapse-target"
              align="center"
              v-on:click.prevent="changeShowMode()"
            >
              <font-awesome-icon
                v-if="!this.showAllInfo"
                icon="caret-down"
              ></font-awesome-icon>
              <font-awesome-icon v-else icon="caret-up"></font-awesome-icon>
            </div>
          </div>
        </div>
        <div
          class="collapse"
          v-bind:id="'collapse-target-investment' + investment.id"
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
      v-bind:modalName="'editInvestmentModal' + investment.id"
      v-bind:investmentId="investment.id"
    >
    </investment-modal>
  </div>
</template>

<script>
import InvestmentModal from "./InvestmentModal.vue";
import { mapActions } from "vuex";

export default {
  components: {
    InvestmentModal,
  },
  data() {
    return {
      showAllInfo: false,
    };
  },
  props: ["investmentId"],
  methods: {
    changeShowMode() {
      this.showAllInfo = !this.showAllInfo;
    },
    ...mapActions("finances", ["deleteInvestment"]),
  },
  computed: {
    investment() {
      return this.$store.getters["finances/getInvestmentById"](
        this.investmentId
      );
    },
  },
};
</script>
