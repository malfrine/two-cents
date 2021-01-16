<template>
  <v-row>
    <v-container>
      <v-col v-for="summary in summaries" :key="summary.name" cols="12">
        <v-card>
          <v-card-title>
            {{ summary.name }}
          </v-card-title>
          <v-divider class="my-1" />
          <v-card-subtitle>
            {{ summary.text }}
          </v-card-subtitle>
        </v-card>
      </v-col>
    </v-container>
  </v-row>
</template>

<script>
export default {
  props: ['selectedStrategy'],
  computed: {
    summaries () {
      return this.$store.getters['plan/getSummaries'](this.selectedStrategy)
    }
  }
}
</script>
