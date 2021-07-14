<template>
  <v-container fill-height fluid>
    <v-row justify="center" align="center">
      <v-col cols="12" md="6">
        <v-card>
          <v-container>
            <v-card-title>
              {{ question }}
            </v-card-title>
            <!-- eslint-disable vue/no-v-html -->
            <v-card-subtitle v-html="information" />
            <!--eslint-enable-->

            <v-container class="pa-4">
              <slot />
            </v-container>
            <v-card-actions>
              <v-spacer />
              <v-btn
                text
                @click="$emit('back')"
              >
                Back
              </v-btn>
              <v-btn
                color="primary"
                @click="$emit('continue')"
              >
                Continue
              </v-btn>
            </v-card-actions>
          </v-container>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  props: {
    question: {
      type: String,
      required: true
    },
    information: {
      type: String,
      default: ''
    }
  }
}
</script>
