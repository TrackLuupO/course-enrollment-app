<!-- StudentRegister.vue -->
<template>
  <div>
    <h2>Register Student</h2>
    <form @submit.prevent="submit">
      <div class="form-group">
        <label>Name</label>
        <input v-model="form.name" required />
      </div>
      <div class="form-group">
        <label>Email</label>
        <input type="email" v-model="form.email" required />
      </div>
      <button type="submit">Register</button>
    </form>
    <p class="message success" v-if="message">{{ message }}</p>
    <p class="message error" v-if="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const api = axios.create({ baseURL: 'http://localhost:8000' })

const form = ref({ name: '', email: '' })
const message = ref('')
const error = ref('')

const submit = async () => {
  try {
    await api.post('/students/', form.value)
    message.value = 'Student registered successfully!'
    form.value = { name: '', email: '' }
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error'
  }
}
</script>