<template>
  <div>
    <form
      @submit.prevent="submitEmail"
      class="input-group bg-transparent center"
      method="post"
      id="email-post-form"
    >
      <div class="container w-75 pt-6">
        <div class="card-body bg-transparent">
          <div class="row">
            <input
              type="email"
              class="form-control rounded-0 col-12 col-sm-8 border"
              placeholder="name@example.com"
              v-model="email"
            >
            <button
              class="btn btn-primary rounded-0 bg-gradient-primary col-12 col-sm-4"
              type="submit"
            >
              Get Notified
            </button>
          </div>
        </div>
      </div>
    </form>

    <p
      class="text-muted text-center mt--3 text-sm ml-1 mr-1"
      id="confirmation-message"
    >
      <em>{{ this.message }}</em>
    </p>
  </div>
</template>

<script>
export default {
  name: 'email-input-form',
  data () {
    return {
      message: '',
      email: ''
    }
  },
  methods: {
    submitEmail () {
      const trimmedEmail = this.email.trim()
      if (trimmedEmail) {
        console.log(this.email) // TODO: post the email
        this.message = "Thanks for signing up! We're excited to save you money!"
        this.email = ''
      }
    }
  }
}
</script>

<style>
</style>
