<template>
  <div>
    <v-tabs color="primary" centered>
      <v-tab>
        <v-icon class="mr-1">
          mdi-account
        </v-icon>
        Profile
      </v-tab>
      <v-tab>
        <v-icon class="mr-1">
          mdi-credit-card-multiple
        </v-icon>
        Loans
      </v-tab>
      <v-tab>
        <v-icon class="mr-1">
          mdi-cash-multiple
        </v-icon>
        Investments
      </v-tab>
      <v-tab>
        <v-icon class="mr-1">
          mdi-trophy
        </v-icon>
        Goals
      </v-tab>

      <v-tab-item>
        <tab-container>
          <ProfileProfileTab class="mx-2 my-2" :read-only="readOnly" :published-plan-id="publishedPlanId" />
        </tab-container>
      </v-tab-item>
      <v-tab-item>
        <tab-container>
          <ProfileLoansTab :read-only="readOnly" :published-plan-id="publishedPlanId" />
        </tab-container>
      </v-tab-item>
      <v-tab-item>
        <tab-container>
          <ProfileInvestmentsTab :read-only="readOnly" :published-plan-id="publishedPlanId" />
        </tab-container>
      </v-tab-item>
      <v-tab-item>
        <tab-container>
          <ProfileGoalsTab :read-only="readOnly" :published-plan-id="publishedPlanId" />
        </tab-container>
      </v-tab-item>
    </v-tabs>
  </div>
</template>

<script>
import ProfileProfileTab from '@/components/dashboard/ProfileProfileTab.vue'
import ProfileInvestmentsTab from '@/components/dashboard/ProfileInvestmentsTab.vue'
import ProfileLoansTab from '@/components/dashboard/ProfileLoansTab.vue'
import ProfileGoalsTab from '@/components/dashboard/ProfileGoalsTab.vue'
import TabContainer from '@/components/base/TabContainer.vue'

export default {
  components: {
    ProfileProfileTab,
    ProfileInvestmentsTab,
    ProfileLoansTab,
    TabContainer,
    ProfileGoalsTab
  },
  props: {
    publishedPlanId: {
      type: Number,
      default: null
    }
  },
  computed: {
    readOnly () {
      return this.publishedPlanId != null
    }
  }
}
</script>

<style>
</style>
