<template>
  <div>
    <div class="text mb-3">
      <div style="font-family: monospace">
        <v-icon large color="primary" class="mb-1">
          {{ `mdi-numeric-${number}-box` }}
        </v-icon>

        {{ category }}
      </div>
    </div>
    <div class="text-h5 text-sm-h4 text-md-h3">
      {{ title }}
    </div>
    <div class="text mt-10">
      {{ mainText }}
    </div>
    <!-- <v-divider class="my-5" /> -->
    <!-- <a :href="learnMoreUrl">
      Learn more
    </a> -->
  </div>
</template>

<script>
export default {
  props: {
    category: {
      type: String,
      default: 'category'
    },
    number: {
      type: Number,
      default: 1
    },
    title: {
      type: String,
      required: true
    },
    mainText: {
      type: String,
      required: true
    },
    learnMoreUrl: {
      type: String,
      default: 'https://blog.two-cents.ca'
    }
  }
}
</script>
