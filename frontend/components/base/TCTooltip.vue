<template>
  <v-tooltip
    fixed
    :top="topOrDefault"
    :right="right"
    :left="left"
    max-width="400"
    open-delay="750"
  >
    <template v-slot:activator="{ on }">
      <div class="pa-0 ma-0" v-on="on">
        <slot name="inner" />
      </div>
    </template>
    <span>{{ text }}</span>
  </v-tooltip>
</template>

<script>

export default {
  props: {
    text: {
      type: String,
      required: true
    },
    top: {
      type: Boolean,
      default: false
    },
    right: {
      type: Boolean,
      default: false
    },
    left: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    topOrDefault () {
      if (!this.top & !this.right & !this.left) {
        return true
      } else {
        return this.top
      }
    }
  }
}
</script>
