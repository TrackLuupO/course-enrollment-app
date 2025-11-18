<template>
  <div id="app">
    <nav class="nav">
      <router-link to="/register-student">Register Student</router-link> |
      <router-link to="/create-course">Create Course</router-link> |
      <router-link to="/enroll">Enroll</router-link> |
      <router-link to="/study-tips">Study Tips</router-link>
    </nav>
    <div class="container">
      <router-view />
    </div>
  </div>
</template>

<script setup>
</script>

<style>
.nav { padding: 20px; background: #2f2f2f; color: white; text-align: center; }
.nav a { color: white; text-decoration: none; margin: 0 15px; font-weight: bold; }
.container { max-width: 800px; margin: 40px auto; padding: 20px; }
</style>