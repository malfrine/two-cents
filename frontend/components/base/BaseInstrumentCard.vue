<template>
  <v-col cols="12" sm="8" md="6" lg="4" xl="3">
    <v-hover v-slot="{ hover }">
      <v-card :elevation="hover ? 4 : 1">
        <slot name="fixed" />
        <v-expand-transition>
          <div v-show="show">
            <v-divider class="mb-5" />
            <slot name="hidden" />
          </div>
        </v-expand-transition>
        <v-card-actions>
          <v-btn
            icon
            @click="show = !show"
          >
            <v-icon>{{ show ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-hover>
  </v-col>
</template>

<script>
export default {
  data: () => ({
    show: false
  })
}
</script>
