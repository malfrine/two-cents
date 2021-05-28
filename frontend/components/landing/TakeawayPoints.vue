<template>
  <div>
    <v-container>
      <v-row justify="center" align="center">
        <v-col cols="12" sm="6">
          <div class="text-center text-sm-left text-h4 my-3">
            Financial planning
            <span class="blue--text font-weight-bold">
              without the fees
            </span>
          </div>
          <div class="text-center text-sm-left text-body-1">
            Everyone deserves a financial plan. Build a free financial plan today in under 15 minutes!
          </div>
        </v-col>
        <v-col cols="12" sm="6">
          <MakeItRainSvg />
        </v-col>
      </v-row>
    </v-container>
    <v-container>
      <v-row justify="center" align="center">
        <v-col cols="12" sm="6" :order="$vuetify.breakpoint.xsOnly ? 1 : 0">
          <v-sheet dark class="pa-10">
            <v-sheet outlined light class="pa-2">
              <PersonalGoalsSvg />
            </v-sheet>
          </v-sheet>
        </v-col>
        <v-col cols="12" sm="6" :order="$vuetify.breakpoint.xsOnly ? 0 : 1">
          <div class="text-center text-sm-left text-h4 my-3">
            A plan built just
            <span class="purple--text font-weight-bold">
              for you
            </span>
          </div>
          <div class="text-center text-sm-left text-body-1">
            You are unique so your financial plan should be unique too. Our AI builds a bespoke plan based on your loans, investments, and financial goals while accounting for your risk tolerance and spending habits.
          </div>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>
