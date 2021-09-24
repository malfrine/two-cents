<template>
  <v-form ref="form">
    <v-btn x-large color="primary" :width="buttonWidth" :small="$vuetify.breakpoint.smAndDown" @click="register()">
      <transition name="fade" mode="out-in">
        <p :key="curTextIndex" class="mb-0">
          {{ buttonText }}
        </p>
      </transition>
    </v-btn>
  </v-form>
</template>

<script>
export default {

  data () {
    const allButtonTexts = [
      'Secure your future',
      'Retire early',
      'Invest wisely',
      'Pay off your loans'
    ]
    const curTextIndex = 0
    return {
      curTextIndex,
      buttonText: allButtonTexts[curTextIndex],
      allButtonTexts,
      intervalSeconds: 2500
    }
  },
  computed: {
    maxIndex () {
      return this.allButtonTexts.length - 1
    },
    buttonWidth () {
      return this.$vuetify.breakpoint.xs ? '90vw' : '400'
    }
  },
  mounted () {
    setInterval(() => {
      this.curTextIndex++
      if (this.curTextIndex > this.maxIndex) {
        this.curTextIndex = 0
      }
      this.buttonText = this.allButtonTexts[this.curTextIndex]
    }, this.intervalSeconds)
  },
  methods: {
    register () {
      this.$router.push('/onboard')
    }
  }
}
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity .7s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
</style>
