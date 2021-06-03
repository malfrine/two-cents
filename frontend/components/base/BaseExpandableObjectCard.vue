<template>
  <v-col cols="12" sm="8" md="6" lg="4" xl="3">
    <v-hover v-slot="{ hover }">
      <v-card :elevation="hover ? 4 : 1">
        <v-row no-gutters>
          <v-col cols="10" class="pa-0">
            <v-card-subtitle class="mb-n7">
              <div class="text-h6">
                <v-icon class="mb-2 mr-2" :color="summaryColor">
                  {{ icon }}
                </v-icon>
                {{ name }}
              </div>
            </v-card-subtitle>
            <v-card-title>
              <div class="text-h2" :style="`color: ${summaryColor}`">
                {{ summaryValue }}
              </div>
            </v-card-title>
          </v-col>
          <v-col cols="2">
            <v-speed-dial
              v-model="fab"
              direction="bottom"
              class="ml-4"
            >
              <template v-slot:activator>
                <v-btn
                  v-model="fab"
                  icon
                  fab
                  small
                  class="mb-n2"
                >
                  <v-icon v-if="fab">
                    mdi-close
                  </v-icon>
                  <v-icon v-else>
                    mdi-dots-horizontal
                  </v-icon>
                </v-btn>
              </template>
              <v-btn
                fab
                small
                color="blue"
                @click.stop="$emit('open-dialog')"
              >
                <v-icon>mdi-pencil</v-icon>
              </v-btn>
              <v-btn
                fab
                small
                color="red"
                @click.prevent="$emit('delete-object')"
              >
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </v-speed-dial>
          </v-col>

          <slot name="dialog" />
        </v-row>

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
  props: {
    name: {
      type: String,
      default: ''
    },
    summaryValue: {
      type: String,
      default: ''
    },
    summaryColor: {
      type: String,
      default: '#25b245'
    },
    icon: {
      type: String,
      default: ''
    }
  },
  data: () => ({
    show: false,
    fab: false
  })
}
</script>
