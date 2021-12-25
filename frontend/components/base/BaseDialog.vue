<template>
  <v-dialog v-model="show" max-width="500px">
    <v-card align="center">
      <v-col cols="12" md="10">
        <div class="text-h6">
          {{ title }}
        </div>
        <v-divider class="my-5" />
        <slot name="form" />
        <v-card-actions class="justify-center">
          <v-btn x-large color="primary" @click="$emit('submit')">
            {{ submitText }}
          </v-btn>
        </v-card-actions>
      </v-col>
    </v-card>
  </v-dialog>
</template>

<script>
// Make sure to $emit the close event

export default {
  props: {
    visible: {
      type: Boolean,
      required: true
    },
    title: {
      type: String,
      required: true
    },
    submitText: {
      type: String,
      default: 'Submit'
    }
  },
  computed: {
    // dialog functionality
    show: {
      get () {
        return this.visible
      },
      set (value) {
        if (!value) {
          this.$emit('close')
        }
      }
    }
  }
}
</script>
