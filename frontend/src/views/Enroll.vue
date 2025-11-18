<template>
  <div>
    <h2>Enroll Student in Course</h2>
    <div class="form-group">
      <label>Student</label>
      <select v-model="student_id" required>
        <option value="">Select student</option>
        <option v-for="s in students" :key="s.id" :value="s.id">{{ s.name }} ({{ s.email }})</option>
      </select>
    </div>
    <div class="form-group">
      <label>Course</label>
      <select v-model="course_id" required>
        <option value="">Select course</option>
        <option v-for="c in courses" :key="c.id" :value="c.id">{{ c.title }} ({{ c.code }})</option>
      </select>
    </div>
    <button @click="enroll">Enroll</button>

    <div v-if="enrolledMessage" class="message success">{{ enrolledMessage }}</div>
    <div v-if="enrolledError" class="message error">{{ enrolledError }}</div>

    <h3 v-if="studentCourses.length">Your enrolled courses:</h3>
    <ul>
      <li v-for="c in studentCourses" :key="c.id">{{ c.title }} – {{ c.credit_units }} credits</li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'
const api = axios.create({ baseURL: 'http://localhost:8000' })

const students = ref([])
const courses = ref([])
const student_id = ref('')
const course_id = ref('')
const enrolledMessage = ref('')
const enrolledError = ref('')
const studentCourses = ref([])

const loadData = async () => {
  const [s, c] = await Promise.all([api.get('/students/'), api.get('/courses/')])
  students.value = s.data
  courses.value = c.data
}

const enroll = async () => {
  try {
    await api.post('/enroll/', { student_id: student_id.value, course_id: course_id.value })
    enrolledMessage.value = 'Enrolled successfully!'
    enrolledError.value = ''
    loadStudentCourses()
  } catch (e) {
    enrolledError.value = e.response?.data?.detail || 'Error'
  }
}

const loadStudentCourses = async () => {
  if (student_id.value) {
    const r = await api.get(`/students/${student_id.value}/courses/`)
    studentCourses.value = r.data
  }
}

onMounted(loadData)
watch(student_id, loadStudentCourses)
</script>