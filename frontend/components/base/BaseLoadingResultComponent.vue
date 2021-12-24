<template>
  <div>
    <v-overlay z-index="2" :value="loading" opacity="0">
      <slot name="loading">
        <v-progress-circular
          :size="150"
          color="primary"
          indeterminate
        />
      </slot>
    </v-overlay>
    <v-overlay z-index="2" :value="error" opacity="0">
      <slot name="error">
        <v-alert
          prominent
          type="error"
          style="max-width: 600px"
        >
          {{ error }}
        </v-alert>
      </slot>
    </v-overlay>
    <slot v-if="success" name="success" />
  </div>
</template>

<script>
export default {
  props: {
    loading: {
      required: true,
      type: Boolean
    },
    error: {
      required: true,
      type: String
    },
    success: {
      required: true,
      type: Boolean
    }
  }
}
</script>

<style>

</style>
