<template>
  <v-card align="center" max-width="500px">
    <v-container class="py-7">
      <v-row justify="center" class="mt-3 mb-5">
        <BigLogo max-height="35" />
      </v-row>
      <div class="text-h5 text-center">
        {{ title }}
      </div>
      <v-card-subtitle v-if="subTitle">
        {{ subTitle }}
      </v-card-subtitle>
      <v-divider class="my-9" />
      <v-container class="px-6">
        <slot />
      </v-container>
    </v-container>
  </v-card>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
      required: true
    },
    subTitle: {
      type: String,
      default: ''
    }
  }
}

</script>
