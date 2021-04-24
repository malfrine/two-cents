<template>
  <div>
    <v-btn
      color="primary"
      x-large
      rounded
      elevation="4"
      @click.stop="dialog = true"
    >
      Join Waitlist
    </v-btn>

    <v-dialog
      v-model="dialog"
      max-width="900"
    >
      <JoinWaitlistForm @form-submitted="dialog = false" />
    </v-dialog>
  </div>
</template>

<script>
import JoinWaitlistForm from '@/components/waitlist/JoinWaitlistForm.vue'

export default {
  components: {
    JoinWaitlistForm
  },
  data () {
    return {
      dialog: false
    }
  }
}
</script>
