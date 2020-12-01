<template>
  <div class="row justify-content-center">
    <div class="col col-lg-8">
      <div class="card bg-secondary shadow border-2 mb-9">
        <div class="card-header pb-4">
          <div class="btn-wrapper text-center col-12">
            <img class="img-fluid" src="../assets/big-logo-dark.png" />
            <div class="container">
              <p
                class="lead text-center text-black mt--2"
                style="font-size: calc(1vw + 1vh + 0.5vmin)"
              >
                DIY financial planning powered by advanced analytics
              </p>
            </div>

            <ComingSoonTimer />

            <ComingSoonInputForm />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ComingSoonTimer from './ComingSoonTimer.vue'
import ComingSoonInputForm from './ComingSoonInputForm.vue'

export default {
  name: 'coming-soon-card',
  components: {
    ComingSoonTimer,
    ComingSoonInputForm
  }
}
</script>

<style>
</style>
