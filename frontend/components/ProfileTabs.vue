<template>
  <section>
    <div
      class="header pb-3 d-flex align-items-center bg-translucent"
    />
    <!-- Tabs Headers-->
    <div class="container-fluid">
      <div class="nav-wrapper">
        <ul
          id="tabs-icons-text"
          class="nav nav-pills nav-fill flex-column flex-md-row"
          role="tablist"
        >
          <li class="nav-item">
            <a
              id="tabs-icons-text-1-tab"
              class="nav-link mb-sm-3 mb-md-0 active"
              data-toggle="tab"
              href="#tabs-icons-text-1"
              role="tab"
              aria-controls="tabs-icons-text-1"
              aria-selected="true"
            >
              <!-- <font-awesome-icon icon="user-astronaut" class="mr-2"></font-awesome-icon> -->
              Profile</a>
          </li>
          <li class="nav-item">
            <a
              id="tabs-icons-text-3-tab"
              class="nav-link mb-sm-3 mb-md-0"
              data-toggle="tab"
              href="#tabs-icons-text-3"
              role="tab"
              aria-controls="tabs-icons-text-3"
              aria-selected="false"
            >
              <!-- <font-awesome-icon icon="money-bill-wave" class="mr-2" /> -->
              Investments</a>
          </li>
          <li class="nav-item">
            <a
              id="tabs-icons-text-4-tab"
              class="nav-link mb-sm-3 mb-md-0"
              data-toggle="tab"
              href="#tabs-icons-text-4"
              role="tab"
              aria-controls="tabs-icons-text-4"
              aria-selected="false"
            >
              <!-- <font-awesome-icon icon="credit-card" class="mr-2" /> -->
              Loans</a>
          </li>
        </ul>
      </div>

      <div class="card shadow">
        <div class="card-body">
          <div id="myTabContent" class="tab-content">
            <div
              id="tabs-icons-text-1"
              class="tab-pane fade show active"
              role="tabpanel"
              aria-labelledby="tabs-icons-text-1-tab"
            >
              <ProfileProfileTab />
            </div>
            <div
              id="tabs-icons-text-3"
              class="tab-pane fade"
              role="tabpanel"
              aria-labelledby="tabs-icons-text-3-tab"
            >
              <ProfileInvestmentsTab />
            </div>
            <div
              id="tabs-icons-text-4"
              class="tab-pane fade"
              role="tabpanel"
              aria-labelledby="tabs-icons-text-4-tab"
            >
              <ProfileLoansTab />
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import ProfileProfileTab from '@/components/ProfileProfileTab.vue'
import ProfileInvestmentsTab from '@/components/ProfileInvestmentsTab.vue'
import ProfileLoansTab from '@/components/ProfileLoansTab.vue'

export default {
  components: {
    ProfileProfileTab,
    ProfileInvestmentsTab,
    ProfileLoansTab
  }
}
</script>

<style>
</style>
