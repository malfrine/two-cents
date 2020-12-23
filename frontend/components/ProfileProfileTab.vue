<template>
  <div class="row">
    <div class="col-12 mb-4">
      <button
        class="btn btn-md btn-primary"
        @click.prevent="toggleEditMode()"
      >
        <v-icon v-if="!this.editMode">mdi-pencil</v-icon>
        <v-icon v-else>mdi-content-save</v-icon>
      </button>
    </div>
    <div class="col">
      <div class="card bg-secondary shadow">
        <div class="card-body">
          <form>
            <!-- Basic User Information-->
            <div class="row align-items-between">
              <div class="col-12 col-sm-10">
                <h6 class="heading-small text-muted">
                  User information
                </h6>
              </div>
            </div>
            <div class="pl-lg-4">
              <div class="row">
                <div class="col-lg-6">
                  <div class="form-group">
                    <label
                      class="form-control-label"
                      for="input-first-name"
                    >First name</label>
                    <input
                      id="input-first-name"
                      v-model="first_name"
                      type="text"
                      class="form-control form-control-alternative"
                      :disabled="true"
                    >
                  </div>
                </div>
                <div class="col-lg-6">
                  <div class="form-group">
                    <label
                      class="form-control-label"
                      for="input-last-name"
                    >Last name</label>
                    <input
                      id="input-last-name"
                      v-model="last_name"
                      type="text"
                      class="form-control form-control-alternative"
                      :disabled="true"
                    >
                  </div>
                </div>
              </div>
              <div class="row">
                <div class="col-lg-6">
                  <div class="form-group">
                    <label
                      class="form-control-label"
                      for="input-birthdate"
                    >Birth Date</label>
                    <input
                      id="input-username"
                      v-model="financial_profile.birth_date"
                      type="date"
                      class="form-control form-control-alternative"
                      placeholder="Username"
                      :disabled="!this.editMode"
                    >
                  </div>
                </div>
                <div class="col-lg-6">
                  <div class="form-group">
                    <label
                      class="form-control-label"
                      for="input-email"
                    >Email address</label>
                    <input
                      id="input-email"
                      v-model="email"
                      type="email"
                      class="form-control form-control-alternative"
                      :disabled="true"
                    >
                  </div>
                </div>
              </div>
            </div>
            <hr class="my-4">
            <!-- Financial Information -->
            <h6 class="heading-small text-muted mb-4">
              Financial information
            </h6>
            <div class="pl-lg-4">
              <div class="row">
                <div class="col-md-6">
                  <div class="form-group">
                    <label
                      class="form-control-label"
                      for="input-monthly-allowance"
                    >Monthly Allowance</label>
                    <div class="input-group mb-3">
                      <div class="input-group-prepend">
                        <span
                          id="basic-addon1"
                          class="input-group-text bg-light"
                        >$</span>
                      </div>
                      <input
                        v-model="financial_profile.monthly_allowance"
                        type="text"
                        class="form-control pl-2"
                        placeholder="1000"
                        aria-label="monthly-allowance"
                        aria-describedby="basic-addon1"
                        :disabled="!this.editMode"
                      >
                    </div>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="form-group">
                    <label
                      class="form-control-label"
                      for="input-retirement-age"
                    >Planned Retirement Age</label>
                    <div class="input-group mb-3">
                      <div class="input-group-prepend">
                        <span
                          id="basic-addon1"
                          class="input-group-text bg-light"
                        >$</span>
                      </div>
                      <input
                        v-model="financial_profile.retirement_age"
                        type="text"
                        class="form-control pl-2"
                        placeholder="65"
                        aria-label="monthly-allowance"
                        aria-describedby="basic-addon1"
                        :disabled="!this.editMode"
                      >
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <hr class="my-4">
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  data () {
    return {
      editMode: false
    }
  },
  computed: {
    financial_profile () {
      return this.$store.getters['finances/getFinancialProfile']
    },
    first_name () {
      return this.$store.getters['finances/getFirstName']
    },
    last_name () {
      return this.$store.getters['finances/getLastName']
    },
    email () {
      return this.$store.getters['finances/getEmail']
    }
  },
  methods: {
    toggleEditMode () {
      if (this.editMode) {
        const fp = {
          birth_date: this.financial_profile.birth_date,
          monthly_allowance: this.financial_profile.monthly_allowance,
          retirement_age: this.financial_profile.retirement_age
        }
        this.$store.dispatch('finances/updateFinancialProfile', fp)
      }
      this.editMode = !this.editMode
    }
  }
}
</script>
