<template>
  <TCTooltip
    :text="tooltipText"
    :top="top"
    :right="right"
    :left="left"
  >
    <template v-slot:inner>
      <v-text-field
        class="my-1"
        outlined
        v-bind="{...$props}"
        v-on="$listeners"
      />
    </template>
  </TCTooltip>
</template>

<script>
import { VTextField } from 'vuetify/lib'
import TCTooltip from '@/components/base/TCTooltip.vue'

export default {
  components: {
    TCTooltip
  },
  extends: VTextField,
  props: {
    tooltipText: {
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
  }
}
</script>
