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

      <v-tab-item>
        <tab-container>
          <ProfileProfileTab class="mx-2 my-2" />
        </tab-container>
      </v-tab-item>
      <v-tab-item>
        <tab-container>
          <ProfileLoansTab />
        </tab-container>
      </v-tab-item>
      <v-tab-item>
        <tab-container>
          <ProfileInvestmentsTab />
        </tab-container>
      </v-tab-item>
    </v-tabs>
  </div>
</template>

<script>
import ProfileProfileTab from '@/components/dashboard/ProfileProfileTab.vue'
import ProfileInvestmentsTab from '@/components/dashboard/ProfileInvestmentsTab.vue'
import ProfileLoansTab from '@/components/dashboard/ProfileLoansTab.vue'
import TabContainer from '@/components/base/TabContainer.vue'

export default {
  components: {
    ProfileProfileTab,
    ProfileInvestmentsTab,
    ProfileLoansTab,
    TabContainer
  }
}
</script>

<style>
</style>
