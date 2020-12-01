<template>
  <div class="container-fluid content-row pt-3">
    <div class="row justify-content-center">
      <div class="col-6 col-sm-3 pb-2">
        <div class="card h-100 pt-2 border-bottom">
          <h2 class="text-black-50 text-center" id="#timer-day"> {{ this.days }} </h2>
          <p class="text-gray-dark text-center text-sm">days</p>
        </div>
      </div>
      <div class="col-6 col-sm-3 pb-2">
        <div class="card h-100 pt-2 border-bottom">
          <h2 class="text-black-50 text-center" id="#timer-hour"> {{ this.hours }} </h2>
          <p class="text-gray-dark text-center text-sm">hours</p>
        </div>
      </div>
      <div class="col-6 col-sm-3 pb-2">
        <div class="card h-100 pt-2 border-bottom">
          <h2 class="text-black-50 text-center" id="#timer-min"> {{ this.minutes }} </h2>
          <p class="text-gray-dark text-center text-sm">minutes</p>
        </div>
      </div>
      <div class="col-6 col-sm-3 pb-2">
        <div class="card h-100 pt-2 border-bottom">
          <h2 class="text-black-50 text-center" id="#timer-sec"> {{ this.seconds }} </h2>
          <p class="text-gray-dark text-center text-sm">seconds</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

var secondsRemaining = (new Date('01 February 2021 00:00:00 GMT').getTime() - new Date().getTime()) / 1000 // seconds

function makeTwoDigitString (s) {
  return s < 10 ? '0' + s : s
}

export default {
  data () {
    return {
      days: '00',
      hours: '00',
      minutes: '00',
      seconds: '00'
    }
  },
  created () {
    console.log('Created timer')
    this.runClock(secondsRemaining)
  },

  methods: {
    runClock (secondsRemaining) {
      setInterval(() => {
        var rem = secondsRemaining
        const seconds = parseInt(rem % 60, 10)
        rem = Math.floor(rem / 60)
        const minutes = parseInt(rem % 60)
        rem = Math.floor(rem / 60)
        const days = parseInt(rem / 24, 10)
        const hours = parseInt(rem % 24, 10)

        this.days = makeTwoDigitString(days)
        this.hours = makeTwoDigitString(hours)
        this.minutes = makeTwoDigitString(minutes)
        this.seconds = makeTwoDigitString(seconds)

        secondsRemaining--
      }, 1000)
    }

  }

}
</script>

<style>
</style>
