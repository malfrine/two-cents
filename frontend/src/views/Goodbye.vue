<template>
  <div>
    <h1>Bye friendo</h1>
    <router-link to="/login" v-on:click.native="postLogout" class="nav-link">
      Take me back.
    </router-link>
  </div>
</template>