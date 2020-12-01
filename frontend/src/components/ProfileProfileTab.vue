<template>
  <div class="row">
    <div class="col-12 mb-4">
      <button
        class="btn btn-md btn-primary"
        v-on:click.prevent="toggleEditMode()"
      >
        <font-awesome-icon
          v-if="!this.editMode"
          icon="edit"
        ></font-awesome-icon>
        <font-awesome-icon v-else icon="save"></font-awesome-icon>
      </button>
    </div>
    <div class="col">
      <div class="card bg-secondary shadow">
        <div class="card-body">
          <form>
            <!-- Basic User Information-->
            <div class="row align-items-between">
              <div class="col-12 col-sm-10">
                <h6 class="heading-small text-muted">User information</h6>
              </div>
            </div>
            <div class="pl-lg-4">
              <div class="row">
                <div class="col-lg-6">
                  <div class="form-group">
                    <label class="form-control-label" for="input-username"
                      >Username</label
                    >
                    <input
                      type="text"
                      id="input-username"
                      class="form-control form-control-alternative"
                      placeholder="Username"
                      v-model="user.username"
                      v-bind:disabled="!this.editMode"
                    />
                  </div>
                </div>
                <div class="col-lg-6">
                  <div class="form-group">
                    <label class="form-control-label" for="input-email"
                      >Email address</label
                    >
                    <input
                      type="email"
                      id="input-email"
                      class="form-control form-control-alternative"
                      v-model="user.email"
                      v-bind:disabled="!this.editMode"
                    />
                  </div>
                </div>
              </div>
              <div class="row">
                <div class="col-lg-6">
                  <div class="form-group">
                    <label class="form-control-label" for="input-first-name"
                      >First name</label
                    >
                    <input
                      type="text"
                      id="input-first-name"
                      class="form-control form-control-alternative"
                      v-model="user.firstname"
                      v-bind:disabled="!this.editMode"
                    />
                  </div>
                </div>
                <div class="col-lg-6">
                  <div class="form-group">
                    <label class="form-control-label" for="input-last-name"
                      >Last name</label
                    >
                    <input
                      type="text"
                      id="input-last-name"
                      class="form-control form-control-alternative"
                      v-model="user.lastname"
                      v-bind:disabled="!this.editMode"
                    />
                  </div>
                </div>
              </div>
            </div>
            <hr class="my-4" />
            <!-- Financial Information -->
            <h6 class="heading-small text-muted mb-4">Financial information</h6>
            <div class="pl-lg-4">
              <div class="row">
                <div class="col-md-6">
                  <div class="form-group">
                    <label
                      class="form-control-label"
                      for="input-monthly-allowance"
                      >Monthly Allowance</label
                    >
                    <div class="input-group mb-3">
                      <div class="input-group-prepend">
                        <span
                          class="input-group-text bg-light"
                          id="basic-addon1"
                          >$</span
                        >
                      </div>
                      <input
                        type="text"
                        class="form-control pl-2"
                        v-model="user.monthlyAllowance"
                        placeholder="monthly-allowance"
                        aria-label="monthly-allowance"
                        aria-describedby="basic-addon1"
                        v-bind:disabled="!this.editMode"
                      />
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <hr class="my-4" />
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  data () {
    return {
      editMode: false
    }
  },
  computed: {
    ...mapGetters('user', { user: ['getUser'] })
  },
  methods: {
    toggleEditMode () {
      if (this.editMode) {
        // save changes
        this.$store.dispatch('user/updateUser', this.user)
      }
      this.editMode = !this.editMode
    }
  }
}
</script>
