<template>
  <simple-layout>
    <div class="container mt--8 pb-9">
      <div class="row justify-content-center">
        <div class="col-lg-6 col-md-8">
          <div class="card shadow">
            <div class="card-header">
              <img
                src="../assets/big-logo-dark.png"
                class="img-fluid"
                alt="Responsive image"
              />
              <h2 class="text-center text-default">Register</h2>
            </div>
            <div class="card-body">
              <form @submit.prevent="handleSubmit">
                <div class="card-body px-lg-5 py-lg-5">
                  <div class="text-muted mb-4">
                    <div class="form-group">
                      <label for="firstname">First Name</label>
                      <input
                        type="text"
                        v-model="firstname"
                        name="firstname"
                        class="form-control"
                      />
                    </div>
                    <div class="form-group">
                      <label for="lastname">Last Name</label>
                      <input
                        type="text"
                        v-model="lastname"
                        name="lastname"
                        class="form-control"
                      />
                    </div>
                    
                    <div class="form-group">
                      <label for="username">Email</label>
                      <input
                        type="text"
                        v-model="email"
                        name="username"
                        class="form-control"
                        :class="{ 'is-invalid': submitted && !email }"
                      />
                      <div
                        v-show="submitted && !email"
                        class="invalid-feedback"
                      >
                        Email is required
                      </div>
                    </div>
                    <div class="form-group">
                      <label htmlFor="password">Password</label>
                      <input
                        type="password"
                        v-model="password"
                        name="password"
                        class="form-control"
                        :class="{ 'is-invalid': submitted && !password }"
                      />
                      <div
                        v-show="submitted && !password"
                        class="invalid-feedback"
                      >
                        Password is required
                      </div>
                    </div>
                    <div class="form-group">
                      <label htmlFor="confirmPassword">Confirm Password</label>
                      <input
                        type="password"
                        v-model="confirmPassword"
                        name="password"
                        class="form-control"
                        :class="{ 'is-invalid': submitted && !confirmPassword }"
                      />
                      <div
                        v-show="submitted && !confirmPassword"
                        class="invalid-feedback"
                      >
                        Password is required
                      </div>
                    </div>
                    <div class="form-group" align="center">
                      <button class="btn btn-primary">Register</button>
                    </div>
                  </div>
                </div>
              </form>
            </div>
            <div class="card-footer"></div>
          </div>
        </div>
      </div>
    </div>
  </simple-layout>
</template>

<script>
import SimpleLayout from "../components/SimpleLayout.vue";
export default {
  components: { SimpleLayout },
  data() {
    return {
      firstname: "",
      lastname: "",
      email: "",
      password: "",
      confirmPassword: "",
      submitted: false,
    };
  },
  methods: {
    validData() {
      return (this.email && this.password.trim() == this.confirmPassword.trim())
    },
    handleSubmit(e) {
      this.submitted = true;
      if (this.validData()) {
        const { email, password, firstname, lastname } = this;
        this.$store.dispatch("auth/postRegister", { email, password, "first_name": firstname, "last_name": lastname });
      }
    },
  },
};
</script>
