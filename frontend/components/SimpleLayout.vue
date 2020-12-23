<template>
<body class="bg-default">

  <div class="main-content">

    <SimpleLayoutNav />

    <SimpleLayoutHeader />

    <div class="container-fluid mt--9 pb--3">
        <slot></slot>
    </div>

  </div>

</body>
</template>

<script>
import SimpleLayoutHeader from '@/components/SimpleLayoutHeader.vue'
import SimpleLayoutNav from '@/components/SimpleLayoutNav.vue'

export default {
  components: {
    SimpleLayoutHeader,
    SimpleLayoutNav
  }
}
</script>
