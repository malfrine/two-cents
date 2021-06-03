<template>
  <TCTooltip :text="text">
    <template v-slot:inner="{ on }">
      <v-icon small class="ml-1 mb-4 mr-1" v-on="on">
        mdi-information-outline
      </v-icon>
    </template>
  </TCTooltip>
</template>

<script>
import TCTooltip from '@/components/base/TCTooltip.vue'

export default {
  components: {
    TCTooltip
  },
  props: {
    text: {
      type: String,
      required: true
    }
  }
}
</script>
