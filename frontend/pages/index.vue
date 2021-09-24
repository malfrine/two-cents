<template>
  <div>
    <v-row justify="center" align="center" class="mt-2 mb-2">
      <v-col cols="11">
        <BigLogo class="mt-6" :max-height="$vuetify.breakpoint.mobile ? '35' : '50'" />
      </v-col>
    </v-row>
    <v-row justify="center" align="center" class="mt-3">
      <v-col cols="12" lg="9" align-self="center">
        <div class="font-weight-bold text-center text-h4 text-sm-h3 text-md-h2 px-2 mb-2">
          Take control of your money
        </div>
        <div class="font-weight-bold text-center grey--text text text-md-h5 px-2">
          Save thousands by planning ahead for your retirement and other life goals
        </div>
      </v-col>
    </v-row>
    <v-row justify="center" class="mt-15">
      <RegisterButton />
    </v-row>
    <v-row align="center" justify="center" class="mt-6">
      <v-col>
        <DashboardExample max-height="800" />
      </v-col>
    </v-row>
    <v-container fluid class="mt-15 mb-10">
      <v-row justify="center" align="center" class="gradient-border-top-bottom">
        <v-container class="py-8 px-6">
          <v-row>
            <v-col v-for="(featurePoint, index) in featurePoints" :key="index" cols="12" md="4">
              <FeaturePointCard :icon-name="featurePoint.iconName" :title="featurePoint.title" :text="featurePoint.text" />
            </v-col>
          </v-row>
        </v-container>
      </v-row>
    </v-container>
    <v-container>
      <div class="text-h6 text-sm-h5 text-md-h4 mb-5 px-8">
        <em>Have you ever wondered...</em>
      </div>
      <template>
        <v-expansion-panels v-model="currentQuestion">
          <v-expansion-panel
            v-for="(question,i) in questions"
            :key="i"
            :class="currentQuestion == i ? 'gradient-border' : null"
          >
            <v-expansion-panel-header>
              <div class="text-sm-h6 line-height">
                {{ question.question }}
              </div>
            </v-expansion-panel-header>
            <v-divider v-if="currentQuestion == i" class="mt-n2 mb-5 px-8" />
            <v-expansion-panel-content>
              {{ question.answer }}
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
      </template>
      <v-row class="pa-3 mt-2" justify="center">
        <div class="text-center text-h6 text-sm-h5 text-md-h4 mt-15 m pa-3">
          We'll help you answer all these questions and more!
        </div>
      </v-row>
      <v-row justify="center" class="mb-15">
        <RegisterButton />
      </v-row>
    </v-container>
    <v-container />
    <PlanSteps />
    <v-spacer style="height: 2vh" />
    <v-row class="pa-3" justify="center">
      <v-col cols="12" md="9" lg="7">
        <div class="text-center text-h6 text-sm-h5 text-md-h4 mt-10 pa-3">
          Get a head start on your financial planning journey!
        </div>
      </v-col>
    </v-row>
    <v-row justify="center" align="center" class="mt-3">
      <RegisterButton />
    </v-row>
    <v-spacer style="height: 10vh" />
  </div>
</template>

<script>
import FeaturePointCard from '@/components/landing/FeaturePointCard.vue'
import BigLogo from '@/components/logo/BigLogo.vue'
import DashboardExample from '@/components/landing/DashboardExample.vue'
import RegisterButton from '@/components/landing/RegisterButton.vue'
import PlanSteps from '@/components/landing/steps/PlanSteps.vue'

export default {
  layout: 'landing',
  components: {
    DashboardExample,
    BigLogo,
    FeaturePointCard,
    RegisterButton,
    PlanSteps
  },
  data () {
    return {
      currentQuestion: null,
      featurePoints: [
        {
          iconName: 'mdi-trophy',
          title: 'Reach your financial goals',
          text: "Whether it's for a down payment on a house, your children's education or saving up for a wedding, we'll help you get there."
        },
        {
          iconName: 'mdi-flag-checkered',
          title: 'Retire early',
          text: 'Find out how much you need to save to achieve the lifestyle you want when you retire.'
        },
        {
          iconName: 'mdi-bank',
          title: 'Get debt free',
          text: 'Get out of the crushing cycle of loan interest and find the best strategy to tackle all your loans.'
        }
      ],
      questions: [
        {
          question: 'With such high house prices, will I ever be able to afford my own home?',
          answer: "Becoming a homeowner has never been tougher and you'll need every advantage you can get. We're here to help you figure out the best saving and investing strategy so that you can buy a home as soon as possible."
        },
        {
          question: 'I have lots of debt. Should I still be investing?',
          answer: "For most people, yes. Only if you have high interest loans (like credit card debt), would it make sense not to invest but everyone is different and you might not like the riskiness of investing. So based on your personal preferences, we'll help you get debt free while minimizing the interest you lose on loan payments."
        },
        {
          question: 'How much should I be putting in my TFSA vs. RRSP?',
          answer: "The tax free savings account (TFSA) and registered retirement savings plan (RRSP) can help you pay less in taxes. Deciding how to split your money between both accounts is a complex decision based on your income growth, your investment portfolio and your expected retirement age. We'll help you navigate this decision to make sure you always come out on top."
        },
        {
          question: 'I have a budget already. Do I still need to be planning?',
          answer: "Yes! Building a budget and sticking to it is only one part of securing your financial health. The other part is making sure your going to meet your long-term goals and that's where we come in!"
        },
        {
          question: 'The stress and pressure of our modern day society is taking its toll on me. When can I sell my worldly positions and live as a recluse in the woods?',
          answer: "We get it. Working 9 to 5 for 40 years is not for everyone. We'll help you plan for your retirement not matter what it'll look like."
        }
      ]
    }
  },
  head () {
    return {
      title: 'Hello, World!'
    }
  }

}
</script>

<style>

.vue-typer .custom.char {
  color: #25b245;
  font-weight: bold;
  word-break: break-all;
}

.vue-typer .custom.caret {
  background-color: #ffffff;
}

.gradient {
  background: linear-gradient(60deg, rgba(37,178,69,1) 0%, rgba(53,163,87,1) 7%, rgba(68,148,105,1) 26%, rgba(84,133,124,1) 44%, rgba(100,117,142,1) 66%, rgba(115,102,160,1) 85%);
}

.gradient-border-top-bottom {
  border-top: 3px solid rgba(37,178,69,1);
  border-bottom: 3px solid rgba(37,178,69,1);
  border-left: 0px solid rgba(37,178,69,1) !important;
  border-right: 0px solid rgba(37,178,69,1) !important;
  border-image: linear-gradient(60deg, rgba(37,178,69,1) 0%, rgba(53,163,87,1) 7%, rgba(68,148,105,1) 26%, rgba(84,133,124,1) 44%, rgba(100,117,142,1) 66%, rgba(115,102,160,1) 85%) 1 stretch;
}

.gradient-border {
  border: 3px solid rgba(37,178,69,1);
  border-image: linear-gradient(60deg, rgba(37,178,69,1) 0%, rgba(53,163,87,1) 7%, rgba(68,148,105,1) 26%, rgba(84,133,124,1) 44%, rgba(100,117,142,1) 66%, rgba(115,102,160,1) 85%) 1 stretch;
}

.line-height {
  line-height: 1.4;
}

</style>
