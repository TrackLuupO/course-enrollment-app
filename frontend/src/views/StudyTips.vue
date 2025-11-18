<template>
  <div>
    <h2>Get Personalized Study Tips</h2>
    <div class="form-group">
      <label>Select Course</label>
      <select v-model="selectedCourseId" @change="loadTips">
        <option value="">Choose a course</option>
        <option v-for="c in courses" :key="c.id" :value="c.id">{{ c.title }} ({{ c.credit_units }} credits)</option>
      </select>
    </div>

    <div v-if="tips.length" class="message success">
      <h3>Tips for {{ selectedTitle }}:</h3>
      <ul>
        <li v-for="(tip, index) in tips" :key="index">{{ tip }}</li>
      </ul>
    </div>
    <div v-if="tipsError" class="message error">{{ tipsError }}</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
const api = axios.create({ baseURL: 'http://localhost:8000' })

const courses = ref([])
const selectedCourseId = ref('')
const selectedTitle = ref('')
const tips = ref([])
const tipsError = ref('')

const loadCourses = async () => {
  const r = await api.get('/courses/')
  courses.value = r.data
}

const loadTips = async () => {
  const course = courses.value.find(c => c.id == selectedCourseId.value)
  if (!course) return
  selectedTitle.value = course.title + ` (${course.credit_units} credits)`
  try {
    const r = await api.post('/genai/study-tips', {
      course_title: course.title,
      credit_units: course.credit_units
    })
    tips.value = r.data.tips
    tipsError.value = ''
  } catch (e) {
    tipsError.value = 'Failed to get tips (check API key?)'
    tips.value = []
  }
}

onMounted(loadCourses)
</script>