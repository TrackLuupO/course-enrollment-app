<template>
  <div>
    <h2>Create New Course</h2>
    <form @submit.prevent="submit">
      <div class="form-group">
        <label>Course Title</label>
        <input v-model="form.title" required />
      </div>

      <div class="form-group">
        <label>Course Code (e.g. MATH101)</label>
        <input v-model="form.code" required />
      </div>

      <div class="form-group">
        <label>Credit Units</label>
        <input type="number" v-model.number="form.credit_units" min="1" required />
      </div>

      <div class="form-group">
        <label>Description (optional)</label>
        <textarea v-model="form.description" rows="3"></textarea>
      </div>

      <button type="submit">Create Course</button>
    </form>

    <p class="message success" v-if="message">{{ message }}</p>
    <p class="message error" v-if="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const api = axios.create({ baseURL: 'http://localhost:8000' })

const form = ref({
  title: '',
  code: '',
  credit_units: 3,
  description: ''
})

const message = ref('')
const error = ref('')

const submit = async () => {
  try {
    await api.post('/courses/', form.value)
    message.value = 'Course created successfully!'
    error.value = ''
    // Reset form
    form.value = { title: '', code: '', credit_units: 3, description: '' }
  } catch (e) {
    error.value = e.response?.data?.detail || 'Failed to create course'
    message.value = ''
  }
}
</script>

<style scoped>
textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-family: inherit;
}
</style>