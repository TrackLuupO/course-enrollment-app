<template>
  <div id="app">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Navigation Bar -->
    <nav class="navbar">
      <div class="nav-brand">
        <i class="fa-solid fa-graduation-cap"></i> Course Enrollment System
      </div>
      <button class="nav-button" @click="showModal = true">
        <i class="fa-solid fa-lightbulb"></i> Study Tips
      </button>
    </nav>

<!-- Loading Overlay -->
<div v-if="isLoading" class="loading-overlay">
  <div class="loading-spinner"></div>
  <p class="loading-text">Loading data...</p>
</div>

    <!-- Main Content -->
    <div class="container">
      <div class="main-content">
        <!-- Home Section -->
        <section class="card">
          <h2 class="section-title">Home</h2>
          <p class="home-description">
            Your journey begins here! <br> Register students and manage courses with ease. Let's transform education together.
          </p>
          <div class="form-container">
            <div class="columns">
              <!-- Name Column -->
              <div>
                <h3 class="column-title">
                  <i class="fa-solid fa-user"></i> Name
                </h3>
                <div class="form-group">
                  <input type="text" class="form-input" placeholder="enter your name" v-model="form.name">
                </div>
                <div class="form-group">
                  <label class="form-label">Email</label>
                  <input type="email" class="form-input" placeholder="enter your email" v-model="form.email">
                </div>
              </div>

              <!-- Course Column -->
              <div>
                <h3 class="column-title">
                  <i class="fa-solid fa-book"></i> Course
                </h3>
                <div class="form-group">
                  <div class="select-wrapper">
                    <select class="form-select" v-model="form.course" @focus="showStudyTip = true" @blur="hideStudyTip">
                      <option value="">Choose a course...</option>
                      <option v-for="course in courses" :key="course.code" :value="course.code">
                        {{ course.code }} - {{ course.title }} ({{ course.credit_units }} CU)
                      </option>
                    </select>
                    <div class="select-arrow">
                      <i class="fa-solid fa-chevron-down"></i>
                    </div>
                  </div>

                  <!-- GenAI Study Tips Floating Card -->
                  <div v-if="showStudyTip && form.course" class="study-tips-floating">
                    <div class="floating-header">
                      <i class="fa-solid fa-robot"></i>
                      <h4>AI Study Tip</h4>
                      <button class="close-tip" @click="showStudyTip = false">&times;</button>
                    </div>
                    <div class="floating-content">
                      <p>{{ currentStudyTip }}</p>
                      <div class="tip-actions">
                        <button class="tip-btn" @click="nextTip">
                          <i class="fa-solid fa-step-forward"></i> Next Tip
                        </button>
                        <button class="tip-btn" @click="saveTip" v-if="!isTipSaved">
                          <i class="fa-solid fa-bookmark"></i> Save
                        </button>
                        <button class="tip-btn saved" v-else disabled>
                          <i class="fa-solid fa-circle-check"></i> Saved
                        </button>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Course Details Preview -->
                <div v-if="selectedCourse" class="course-preview">
                  <div class="preview-card">
                    <h4 class="preview-title">{{ selectedCourse.title }}</h4>
                    <div class="preview-details">
                      <span class="course-code">{{ selectedCourse.code }}</span>
                      <span class="credit-units">{{ selectedCourse.credit_units }} Credit Units</span>
                    </div>
                    <p class="course-description">{{ selectedCourse.description }}</p>

                    <!-- Saved Study Tips for this Course -->
                    <div v-if="savedTips.length > 0" class="saved-tips-section">
                      <div class="saved-tips-header">
                        <i class="fa-solid fa-bookmark"></i>
                        <h5>Your Saved Study Tips</h5>
                      </div>
                      <div class="saved-tips-list">
                        <div v-for="(tip, index) in savedTips" :key="index" class="saved-tip-item">
                          <p>{{ tip }}</p>
                          <button class="remove-tip" @click="removeTip(index)">
                            <i class="fa-solid fa-times"></i>
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Register Student Button -->
                <button class="btn btn-full" @click="registerStudent">
                  <i class="fa-solid fa-user-plus"></i> Register Student
                </button>

                <!-- View All Students Button -->
                <button class="btn-outline btn-full" @click="openStudentsListModal">
                  <i class="fa-solid fa-users"></i> View All Students
                </button>
              </div>
            </div>
          </div>
        </section>

        <!-- Divider -->
        <div class="divider"></div>

        <!-- NEW: Course Management Section -->
        <section class="card">
          <h2 class="section-title section-title-center">Course Management</h2>

          <div class="course-management-container">
            <div class="management-actions">
              <button class="btn" @click="showCreateCourseForm = !showCreateCourseForm">
                <i class="fa-solid fa-circle-check"></i> {{ showCreateCourseForm ? 'Cancel' : 'Create Course' }}
              </button>
              <button class="btn-outline" @click="openAllCoursesModal">
                <i class="fa-solid fa-list"></i> View All Courses
              </button>
            </div>

            <!-- Create Course Form -->
            <div v-if="showCreateCourseForm" class="create-course-form">
              <div class="form-grid">
                <div class="form-group">
                  <label class="form-label">Course Title</label>
                  <input type="text" class="form-input" placeholder="Enter course title" v-model="newCourse.title">
                </div>

                <div class="form-group">
                  <label class="form-label">Course Code</label>
                  <input type="text" class="form-input" placeholder="e.g., CS101" v-model="newCourse.code">
                </div>

                <div class="form-group">
                  <label class="form-label">Credit Units</label>
                  <div class="select-wrapper">
                    <select class="form-select" v-model="newCourse.credit_units">
                      <option value="">Select credit units</option>
                      <option value="1">1 Credit Unit</option>
                      <option value="2">2 Credit Units</option>
                      <option value="3">3 Credit Units</option>
                      <option value="4">4 Credit Units</option>
                      <option value="5">5 Credit Units</option>
                    </select>
                    <div class="select-arrow">
                      <i class="fa-solid fa-chevron-down"></i>
                    </div>
                  </div>
                </div>
              </div>

              <div class="form-group">
                <label class="form-label">Course Description</label>
                <textarea class="form-textarea" placeholder="Enter course description" v-model="newCourse.description" rows="3"></textarea>
              </div>

              <div class="form-actions">
                <button class="btn btn-full" @click="createCourse" :disabled="!isCourseFormValid">
                  <i class="fa-solid fa-save"></i> Save Course
                </button>
              </div>
            </div>

            <!-- Recently Added Courses Preview -->
            <div v-if="recentCourses.length > 0" class="recent-courses">
              <h3 class="sub-section-title">
                <i class="fa-solid fa-history"></i> Recently Added Courses
              </h3>
              <div class="recent-courses-grid">
                <div v-for="course in recentCourses" :key="course.code" class="recent-course-card">
                  <div class="recent-course-header">
                    <h4>{{ course.title }}</h4>
                    <span class="course-code-small">{{ course.code }}</span>
                  </div>
                  <div class="recent-course-body">
                    <p class="course-description-small">{{ course.description }}</p>
                  </div>
                  <div class="recent-course-footer">
                    <span class="credit-units-small">{{ course.credit_units }} CU</span>
                    <span class="course-date">Added: {{ formatDate(course.createdAt) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- Divider -->
        <div class="divider"></div>

        <!-- Enroll Section -->
        <section class="card">
          <h2 class="section-title section-title-center">Enroll</h2>

          <div class="enroll-form-container">
            <!-- Select Student -->
            <div class="form-group">
              <div class="form-header">
                <label class="form-label">Select Student</label>
              </div>
              <div class="select-wrapper">
                <select class="form-select" v-model="enrollment.student">
                  <option value="">Choose a student...</option>
                  <option v-for="student in availableStudents" :key="student.id" :value="student.id">
                    {{ student.name }} ({{ student.email }})
                  </option>
                </select>
                <div class="select-arrow">
                  <i class="fa-solid fa-chevron-down"></i>
                </div>
              </div>
            </div>

            <!-- Select Course -->
            <div class="form-group">
              <div class="form-header">
                <label class="form-label">Select Course</label>
              </div>
              <div class="select-wrapper">
                <select class="form-select" v-model="enrollment.course">
                  <option value="">Choose a course...</option>
                  <option v-for="course in availableCourses" :key="course.code" :value="course.code">
                    {{ course.code }} - {{ course.title }} ({{ course.credit_units }} CU)
                  </option>
                </select>
                <div class="select-arrow">
                  <i class="fa-solid fa-chevron-down"></i>
                </div>
              </div>
            </div>

            <!-- Course Details Preview for Enroll Section -->
            <div v-if="enrolledCourse" class="course-preview">
              <div class="preview-card">
                <h4 class="preview-title">{{ enrolledCourse.title }}</h4>
                <div class="preview-details">
                  <span class="course-code">{{ enrolledCourse.code }}</span>
                  <span class="credit-units">{{ enrolledCourse.credit_units }} Credit Units</span>
                </div>
                <p class="course-description">{{ enrolledCourse.description }}</p>
              </div>
            </div>

            <!-- Enroll Button -->
            <button class="btn btn-full" @click="enrollStudent">Enroll</button>
          </div>
        </section>

        <!-- Quick Stats Section -->
        <section class="card stats-card">
          <h2 class="section-title">Quick Overview</h2>
          <div class="stats-grid">
            <div class="stat-item" @click="viewAllStudents">
              <div class="stat-icon">
                <i class="fa-solid fa-user-graduate"></i>
              </div>
              <div class="stat-info">
                <h3>{{ allStudents.length }}</h3>
                <p>Registered Students</p>
              </div>
            </div>
            <div class="stat-item" @click="viewAllCourses">
              <div class="stat-icon">
                <i class="fa-solid fa-book-open"></i>
              </div>
              <div class="stat-info">
                <h3>{{ courses.length }}</h3>
                <p>Available Courses</p>
              </div>
            </div>
            <div class="stat-item" @click="viewAllEnrollments">
              <div class="stat-icon">
                <i class="fa-solid fa-clipboard-list"></i>
              </div>
              <div class="stat-info">
                <h3>{{ totalEnrollments }}</h3>
                <p>Total Enrollments</p>
              </div>
            </div>
          </div>
        </section>
      </div>
                <!-- Connection Status Indicator -->
                <div :class="['connection-status', isBackendConnected ? 'connected' : 'disconnected']">
                  <i :class="isBackendConnected ? 'fa-solid fa-circle-check' : 'fa-solid fa-circle-exclamation'"></i>
                  {{ isBackendConnected ? 'Backend Connected' : 'Backend Disconnected' }}
                </div>
                <!-- Toast Notification -->
                <div v-if="toast.show" class="toast-notification" :class="toast.type">
                  <i :class="toast.icon"></i>
                <div>
                  <strong>{{ toast.title }}</strong>
                  <p style="margin: 4px 0 0; font-size: 0.9rem;">{{ toast.message }}</p>
                </div>
                <button @click="toast.show = false" style="margin-left: auto; background: none; color: #64748b; padding: 4px;">
                  <i class="fa-solid fa-times"></i>
                </button>
      </div>
    </div>

    <!-- Footer -->
    <div class="footer">
      <p>Course Enrollment System &copy; 2025. All rights reserved.</p>
    </div>

    <!-- Students List Modal -->
    <div class="modal" v-if="showStudentsListModal" @click="closeStudentsListModal">
      <div class="modal-content list-modal" @click.stop>
        <button class="close-modal" @click="closeStudentsListModal">&times;</button>
        <div class="modal-header">
          <i class="fa-solid fa-user-graduate modal-header-icon"></i>
          <h2 class="section-title">All Registered Students</h2>
        </div>

        <div class="students-table-container">
          <table class="students-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="student in allStudents" :key="student.id" class="student-row">
                <td class="student-id">{{ student.id }}</td>
                <td class="student-name">
                  <div class="student-name-wrapper">
                    <i class="fa-solid fa-user student-icon"></i>
                    {{ student.name }}
                  </div>
                </td>
                <td class="student-email">{{ student.email }}</td>
                <td class="student-actions">
                  <button class="view-courses-btn" @click="viewStudentCoursesFromList(student)">
                    <i class="fa-solid fa-book-open"></i> View Courses
                  </button>
                </td>
              </tr>
            </tbody>
          </table>

          <div v-if="allStudents.length === 0" class="empty-state">
            <i class="fa-solid fa-user-slash empty-icon"></i>
            <p>No students registered yet</p>
          </div>
        </div>

        <div class="modal-footer">
          <div class="total-students">
            <i class="fa-solid fa-chart-bar"></i>
            <span>Total Students: {{ allStudents.length }}</span>
          </div>
          <button class="btn close-btn" @click="closeStudentsListModal">Close</button>
        </div>
      </div>
    </div>

    <!-- All Courses Modal -->
    <div class="modal" v-if="showAllCoursesModal" @click="closeAllCoursesModal">
      <div class="modal-content list-modal" @click.stop>
        <button class="close-modal" @click="closeAllCoursesModal">&times;</button>
        <div class="modal-header">
          <i class="fa-solid fa-book-open modal-header-icon"></i>
          <h2 class="section-title">All Available Courses</h2>
        </div>

        <div class="list-container">
          <div v-for="course in courses" :key="course.code" class="list-item">
            <div class="list-item-main">
              <div class="course-info">
                <h4>{{ course.title }}</h4>
                <span class="course-code">{{ course.code }}</span>
              </div>
              <div class="course-actions">
                <button class="view-students-btn" @click="viewCourseStudentsFromCourse(course)" style="background: #10b981; margin-right: 5px;">
                  <i class="fa-solid fa-users"></i> Students
                </button>
                <button class="edit-course-btn" @click="editCourse(course)">
                  <i class="fa-solid fa-edit"></i> Edit
                </button>
                <button class="delete-course-btn" @click="deleteCourse(course.code)">
                  <i class="fa-solid fa-trash"></i> Delete
                </button>
              </div>
            </div>
            <div class="list-item-meta">
              <span class="credit-units">{{ course.credit_units }} CU</span>
              <span class="student-count">{{ getCourseStudentCount(course.code) }} students</span>
              <span class="course-date" v-if="course.createdAt">Added: {{ formatDate(course.createdAt) }}</span>
            </div>
            <div class="course-description-modal">
              <p>{{ course.description }}</p>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <div class="total-courses">
            <i class="fa-solid fa-chart-bar"></i>
            <span>Total Courses: {{ courses.length }}</span>
          </div>
          <button class="btn close-btn" @click="closeAllCoursesModal">Close</button>
        </div>
      </div>
    </div>

    <!-- Study Tips Modal -->
    <div class="modal" v-if="showModal" @click="closeModal">
      <div class="modal-content" @click.stop>
        <button class="close-modal" @click="showModal = false">&times;</button>
        <div class="modal-header">
          <i class="fa-solid fa-lightbulb modal-header-icon"></i>
          <h2 class="section-title">Study Tips & Strategies</h2>
        </div>

        <ul class="study-tips-list">
          <li class="study-tip">
            <span class="bullet-point"></span>
            <span><strong>Active Recall:</strong> Test yourself regularly instead of just re-reading. This strengthens memory retention significantly.</span>
          </li>
          <li class="study-tip">
            <span class="bullet-point"></span>
            <span><strong>Spaced Repetition:</strong> Review material at increasing intervals to combat the forgetting curve.</span>
          </li>
          <li class="study-tip">
            <span class="bullet-point"></span>
            <span><strong>Pomodoro Technique:</strong> Study in focused 25-minute blocks with 5-minute breaks to maintain peak concentration.</span>
          </li>
          <li class="study-tip">
            <span class="bullet-point"></span>
            <span><strong>Interleaving:</strong> Mix different subjects or topics during study sessions to improve learning flexibility.</span>
          </li>
          <li class="study-tip">
            <span class="bullet-point"></span>
            <span><strong>Teach What You Learn:</strong> Explain concepts to others to identify gaps in your understanding.</span>
          </li>
          <li class="study-tip">
            <span class="bullet-point"></span>
            <span><strong>Create Mind Maps:</strong> Visualize connections between concepts to enhance comprehension and recall.</span>
          </li>
        </ul>

        <div class="tip-box">
          <div class="tip-header">
            <i class="fa-solid fa-graduation-cap tip-icon"></i>
            <h3 class="tip-title">Effective Study Environment</h3>
          </div>
          <p class="tip-content">Choose a quiet, well-lit space dedicated to studying. Keep your study area organized and free from distractions like phones and social media. Natural light and proper ergonomics can significantly improve focus and productivity.</p>
        </div>

        <div class="tip-box">
          <div class="tip-header">
            <i class="fa-solid fa-brain tip-icon"></i>
            <h3 class="tip-title">Memory Enhancement Techniques</h3>
          </div>
          <p class="tip-content">Use mnemonic devices, create associations with existing knowledge, and practice retrieval through flashcards. Sleep plays a crucial role in memory consolidation, so ensure you get 7-9 hours of quality sleep during intensive study periods.</p>
        </div>

        <div class="tip-box">
          <div class="tip-header">
            <i class="fa-solid fa-clock tip-icon"></i>
            <h3 class="tip-title">Time Management</h3>
          </div>
          <p class="tip-content">Create a weekly study schedule that allocates specific time blocks for each subject. Prioritize difficult topics when your energy levels are highest, and include regular review sessions to reinforce learning.</p>
        </div>

        <div class="tip-box">
          <div class="tip-header">
            <i class="fa-solid fa-heart tip-icon"></i>
            <h3 class="tip-title">Health & Wellness</h3>
          </div>
          <p class="tip-content">Stay hydrated, eat nutritious meals, and incorporate physical activity into your routine. Taking care of your physical health directly impacts cognitive performance, memory retention, and overall academic success.</p>
        </div>
      </div>
    </div>

    <!-- Success Modal -->
    <div class="modal" v-if="showSuccessModal" @click="closeSuccessModal">
      <div class="modal-content success-modal" @click.stop>
        <div class="success-icon">
          <i class="fa-solid fa-circle-check"></i>
        </div>
        <h2 class="success-title">{{ successTitle }}</h2>
        <p class="success-message">{{ successMessage }}</p>
        <button class="btn success-btn" @click="closeSuccessModal">Continue</button>
      </div>
    </div>

    <!-- Error Modal -->
    <div class="modal" v-if="showErrorModal" @click="closeErrorModal">
      <div class="modal-content error-modal" @click.stop>
        <div class="error-icon">
          <i class="fa-solid fa-exclamation-circle"></i>
        </div>
        <h2 class="error-title">{{ errorTitle }}</h2>
        <p class="error-message">{{ errorMessage }}</p>
        <button class="btn error-btn" @click="closeErrorModal">Okay</button>
      </div>
    </div>

    <!-- Student Courses Modal -->
    <div class="modal" v-if="showStudentCoursesModal" @click="closeStudentCoursesModal">
      <div class="modal-content list-modal" @click.stop>
        <button class="close-modal" @click="closeStudentCoursesModal">&times;</button>
        <div class="modal-header">
          <i class="fa-solid fa-user-graduate modal-header-icon"></i>
          <h2 class="section-title">{{ selectedStudentForCourses ? selectedStudentForCourses.name + "'s Courses" : 'Student Courses' }}</h2>
        </div>

        <div v-if="studentCoursesList.length > 0" class="list-container">
          <div v-for="course in studentCoursesList" :key="course.code" class="list-item">
            <div class="list-item-main">
              <h4>{{ course.title }}</h4>
              <span class="course-code">{{ course.code }}</span>
            </div>
            <div class="list-item-meta">
              <span class="credit-units">{{ course.credit_units }} CU</span>
              <span class="enrollment-date">Enrolled: {{ getEnrollmentDate(course.code) }}</span>
            </div>
          </div>
        </div>
        <div v-else class="empty-state">
          <i class="fa-solid fa-book-open empty-icon"></i>
          <p>No courses enrolled yet</p>
        </div>
      </div>
    </div>

    <!-- Course Students Modal -->
    <div class="modal" v-if="showCourseStudentsModal" @click="closeCourseStudentsModal">
      <div class="modal-content list-modal" @click.stop>
        <button class="close-modal" @click="closeCourseStudentsModal">&times;</button>
        <div class="modal-header">
          <i class="fa-solid fa-users modal-header-icon"></i>
          <h2 class="section-title">{{ selectedCourseForStudents ? selectedCourseForStudents.title + ' - Students' : 'Course Students' }}</h2>
        </div>

        <div v-if="courseStudentsList.length > 0" class="list-container">
          <div v-for="student in courseStudentsList" :key="student.id" class="list-item">
            <div class="list-item-main">
              <h4>{{ student.name }}</h4>
              <span class="student-email">{{ student.email }}</span>
            </div>
            <div class="list-item-meta">
              <span class="enrollment-date">Enrolled: {{ getEnrollmentDate(selectedCourseForStudents.code, student.id) }}</span>
            </div>
          </div>
        </div>
        <div v-else class="empty-state">
          <i class="fa-solid fa-user-slash empty-icon"></i>
          <p>No students enrolled yet</p>
        </div>
      </div>
    </div>

    <!-- Edit Course Modal -->
    <div class="modal" v-if="showEditCourseModal" @click="closeEditCourseModal">
      <div class="modal-content" @click.stop>
        <button class="close-modal" @click="closeEditCourseModal">&times;</button>
        <div class="modal-header">
          <i class="fa-solid fa-edit modal-header-icon"></i>
          <h2 class="section-title">Edit Course</h2>
        </div>

        <div class="create-course-form">
          <div class="form-grid">
            <div class="form-group">
              <label class="form-label">Course Title</label>
              <input type="text" class="form-input" placeholder="Enter course title" v-model="editingCourse.title">
            </div>

            <div class="form-group">
              <label class="form-label">Course Code</label>
              <input type="text" class="form-input" placeholder="e.g., CS101" v-model="editingCourse.code" :disabled="true">
              <small class="form-hint">Course code cannot be changed</small>
            </div>

            <div class="form-group">
              <label class="form-label">Credit Units</label>
              <div class="select-wrapper">
                <select class="form-select" v-model="editingCourse.credit_units">
                  <option value="">Select credit units</option>
                  <option value="1">1 Credit Unit</option>
                  <option value="2">2 Credit Units</option>
                  <option value="3">3 Credit Units</option>
                  <option value="4">4 Credit Units</option>
                  <option value="5">5 Credit Units</option>
                </select>
                <div class="select-arrow">
                  <i class="fa-solid fa-chevron-down"></i>
                </div>
              </div>
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">Course Description</label>
            <textarea class="form-textarea" placeholder="Enter course description" v-model="editingCourse.description" rows="4"></textarea>
          </div>

          <div class="form-actions">
            <button class="btn btn-full" @click="updateCourse" :disabled="!isEditFormValid">
              <i class="fa-solid fa-save"></i> Update Course
            </button>
            <button class="btn-outline btn-full" @click="closeEditCourseModal">
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { api } from './services/api';

export default {
  name: 'App',
  data() {
    return {
      // Modals - keep existing
      showModal: false,
      showSuccessModal: false,
      showErrorModal: false,
      showStudentCoursesModal: false,
      showCourseStudentsModal: false,
      showAllCoursesModal: false,
      showStudentsListModal: false,
      showEditCourseModal: false,
      
      // Course Management
      showCreateCourseForm: false,
      newCourse: {
        title: '',
        code: '',
        credit_units: '',
        description: ''
      },
      
      // Edit Course
      editingCourse: {
        id: null,
        title: '',
        code: '',
        credit_units: '',
        description: ''
      },
      
      successTitle: '',
      successMessage: '',
      errorTitle: '',
      errorMessage: '',
      
      // GenAI Study Tips Feature
      showStudyTip: false,
      currentStudyTip: '',
      currentTipIndex: 0,
      isTipSaved: false,
      savedTips: [],
      
      form: {
        name: '',
        email: '',
        course: ''
      },
      enrollment: {
        student: '',
        course: ''
      },
      
      // Data from backend - INITIALIZE AS EMPTY
      students: [],
      courses: [],
      enrollments: [], // NEW: Store enrollments
      
      // Lists for modals
      studentCoursesList: [],
      courseStudentsList: [],
      selectedStudentForCourses: null,
      selectedCourseForStudents: null,
      
      // Statistics
      statistics: {
        total_students: 0,
        total_courses: 0,
        total_enrollments: 0
      },
      
      // Loading states
      isLoading: false,

      // Connection Status (NEW)
      isBackendConnected: false,
    
      // Toast Notifications (NEW)
      toast: {
        show: false,
        title: '',
        message: '',
        type: 'info', // 'info', 'success', 'error'
        icon: 'fa-solid fa-info-circle'
      }
    } 
  },
  computed: {
    selectedCourse() {
      if (!this.courses || !Array.isArray(this.courses)) return null;
      return this.courses.find(course => course.code === this.form.course);
    },
    enrolledCourse() {
      if (!this.courses || !Array.isArray(this.courses)) return null;
      return this.courses.find(course => course.code === this.enrollment.course);
    },
    allStudents() {
      return this.students || [];
    },
    availableStudents() {
      return this.students || [];
    },
    availableCourses() {
      return this.courses || [];
    },
    totalEnrollments() {
      return (this.statistics && this.statistics.total_enrollments) || 0;
    },
    isCourseFormValid() {
      return (
        this.newCourse.title.trim() !== '' &&
        this.newCourse.code.trim() !== '' &&
        this.newCourse.credit_units !== '' &&
        this.newCourse.description.trim() !== ''
      );
    },
    isEditFormValid() {
      return (
        this.editingCourse.title.trim() !== '' &&
        this.editingCourse.code.trim() !== '' &&
        this.editingCourse.credit_units !== '' &&
        this.editingCourse.description.trim() !== ''
      );
    },
    recentCourses() {
      if (!this.courses || !Array.isArray(this.courses)) {
        return [];
      }
      return [...this.courses]
        .sort((a, b) => b.id - a.id)
        .slice(0, 3);
    },
    // Get course student count from enrollments
    courseStudentCounts() {
      const counts = {};
      this.enrollments.forEach(enrollment => {
        if (!counts[enrollment.course_id]) {
          counts[enrollment.course_id] = 0;
        }
        counts[enrollment.course_id]++;
      });
      return counts;
    }
  },
  methods: {
    // Load all data from backend
    async loadAllData() {
      this.isLoading = true;
      try {
        console.log('🔄 Loading data from backend...');
        const [students, courses, enrollments, stats] = await Promise.all([
          api.getStudents(),
          api.getCourses(),
          api.getEnrollments(),
          api.getStatistics()
        ]);
        
        this.students = students;
        this.courses = courses;
        this.enrollments = enrollments;
        this.statistics = stats;
        
        console.log('✅ Data loaded:', {
          students: this.students.length,
          courses: this.courses.length,
          enrollments: this.enrollments.length,
          stats: this.statistics
        });
      } catch (error) {
        console.error('❌ Error loading data:', error);
        this.showError('Connection Error', 'Failed to connect to backend. Make sure the server is running on http://localhost:8000');
      } finally {
        this.isLoading = false;
      }
    },

    // Register Student
    async registerStudent() {
      if (!this.form.name || !this.form.email || !this.form.course) {
        this.showError('Incomplete Form', 'Please fill in all fields to complete registration.');
        return;
      }

      try {
        const selectedCourse = this.courses.find(c => c.code === this.form.course);
        if (!selectedCourse) {
          this.showError('Course Not Found', 'Selected course does not exist.');
          return;
        }

        // 1. Create student
        const studentData = {
          name: this.form.name,
          email: this.form.email
        };

        const studentResponse = await api.createStudent(studentData);
        console.log('✅ Student created:', studentResponse);

        // 2. Enroll student in course
        const enrollmentData = {
          student_id: studentResponse.id,
          course_id: selectedCourse.id
        };

        await api.createEnrollment(enrollmentData);
        console.log('✅ Enrollment created');

        // 3. Refresh all data
        await this.loadAllData();

        // 4. Show success
        this.showSuccess(
          'Registration Successful!',
          `Congratulations ${this.form.name}, you have been registered for ${selectedCourse.title}!`
        );

        // 5. Reset form
        this.form = { name: '', email: '', course: '' };
        this.showStudyTip = false;

      } catch (error) {
        console.error('❌ Registration error:', error);
        this.showError('Registration Failed', error.message || 'Failed to register student.');
      }
    },

    // Create Course
    async createCourse() {
      if (!this.isCourseFormValid) {
        this.showError('Incomplete Form', 'Please fill in all course fields.');
        return;
      }

      try {
        const courseData = {
          title: this.newCourse.title,
          code: this.newCourse.code.toUpperCase(),
          credit_units: parseInt(this.newCourse.credit_units),
          description: this.newCourse.description
        };

        const response = await api.createCourse(courseData);
        console.log('✅ Course created:', response);

        // Refresh data
        await this.loadAllData();

        // Show success
        this.showSuccess('Course Created!', 
          `Course "${response.title}" (${response.code}) has been successfully added.`);

        // Reset form
        this.newCourse = {
          title: '',
          code: '',
          credit_units: '',
          description: ''
        };
        this.showCreateCourseForm = false;

      } catch (error) {
        console.error('❌ Course creation error:', error);
        this.showError('Course Creation Failed', error.message || 'Failed to create course.');
      }
    },

    // Update Course
    async updateCourse() {
      if (!this.isEditFormValid) {
        this.showError('Incomplete Form', 'Please fill in all course fields.');
        return;
      }

      try {
        const courseData = {
          title: this.editingCourse.title,
          code: this.editingCourse.code,
          credit_units: parseInt(this.editingCourse.credit_units),
          description: this.editingCourse.description
        };

        const response = await api.updateCourse(this.editingCourse.id, courseData);
        console.log('✅ Course updated:', response);

        // Refresh data
        await this.loadAllData();

        // Show success
        this.showSuccess('Course Updated!', 
          `Course "${response.title}" (${response.code}) has been successfully updated.`);

        // Close modal
        this.closeEditCourseModal();

      } catch (error) {
        console.error('❌ Course update error:', error);
        this.showError('Update Failed', error.message || 'Failed to update course.');
      }
    },

    // Delete Course
    async deleteCourse(courseCode) {
      const course = this.courses.find(c => c.code === courseCode);
      if (!course) return;

      // Check if course has enrollments
      const courseEnrollments = this.enrollments.filter(e => e.course_id === course.id);
      if (courseEnrollments.length > 0) {
        this.showError('Cannot Delete Course', 
          `This course has ${courseEnrollments.length} enrolled student(s). Please unenroll all students first.`);
        return;
      }

      if (!confirm(`Are you sure you want to delete course "${courseCode}"?`)) {
        return;
      }

      try {
        await api.deleteCourse(course.id);
        console.log('✅ Course deleted');

        // Refresh data
        await this.loadAllData();

        // Show success
        this.showSuccess('Course Deleted!', 
          `Course "${courseCode}" has been removed from the system.`);

      } catch (error) {
        console.error('❌ Course deletion error:', error);
        this.showError('Deletion Failed', error.message || error.detail || 'Failed to delete course.');
      }
    },

    // Enroll Student (from Enroll section)
    async enrollStudent() {
      if (!this.enrollment.student || !this.enrollment.course) {
        this.showError('Incomplete Selection', 'Please select both student and course.');
        return;
      }

      const student = this.students.find(s => s.id === parseInt(this.enrollment.student));
      const course = this.courses.find(c => c.code === this.enrollment.course);

      if (!student || !course) {
        this.showError('Not Found', 'Student or course not found.');
        return;
      }

      try {
        const enrollmentData = {
          student_id: student.id,
          course_id: course.id
        };

        await api.createEnrollment(enrollmentData);
        console.log('✅ Enrollment created');

        // Refresh data
        await this.loadAllData();

        // Show success
        this.showSuccess('Enrollment Successful!', 
          `${student.name} has been enrolled in ${course.title}!`);

        // Reset form
        this.enrollment = { student: '', course: '' };

      } catch (error) {
        console.error('❌ Enrollment error:', error);
        this.showError('Enrollment Failed', error.message || 'Failed to enroll student.');
      }
    },

    // Load Student Courses
    async loadStudentCourses(studentId) {
      try {
        const response = await api.getStudentEnrollments(studentId);
        this.studentCoursesList = response.map(item => item.course);
      } catch (error) {
        console.error('❌ Error loading student courses:', error);
        this.showError('Error', 'Failed to load student courses.');
      }
    },

    // Load Course Students
    async loadCourseStudents(courseId) {
      try {
        const response = await api.getCourseEnrollments(courseId);
        this.courseStudentsList = response.map(item => item.student);
      } catch (error) {
        console.error('❌ Error loading course students:', error);
        this.showError('Error', 'Failed to load enrolled students.');
      }
    },

    // View Student Courses (from Students List)
    async viewStudentCoursesFromList(student) {
      this.selectedStudentForCourses = student;
      await this.loadStudentCourses(student.id);
      this.closeStudentsListModal();
      this.showStudentCoursesModal = true;
    },

    // View Course Students
    async viewCourseStudentsFromCourse(course) {
      this.selectedCourseForStudents = course;
      await this.loadCourseStudents(course.id);
      this.closeAllCoursesModal();
      this.showCourseStudentsModal = true;
    },

    // Get course student count
    getCourseStudentCount(courseCode) {
      const course = this.courses.find(c => c.code === courseCode);
      if (!course) return 0;
      return this.enrollments.filter(e => e.course_id === course.id).length;
    },

    // Edit Course
    editCourse(course) {
      this.editingCourse = {
        id: course.id,
        title: course.title,
        code: course.code,
        credit_units: course.credit_units.toString(),
        description: course.description || ''
      };
      this.showAllCoursesModal = false;
      this.showEditCourseModal = true;
    },

    // Test Backend Connection
    async testBackendConnection() {
      try {
        const result = await api.testConnection();
        console.log('✅ Connection test:', result);
        alert(`Backend Status: ${result.message}`);
      } catch (error) {
        console.error('❌ Connection test failed:', error);
        alert(`Connection Failed: ${error.message}`);
      }
    },

    // Keep existing modal methods (they don't need to change)
    // Keep existing modal methods (they don't need to change)
    showSuccess(title, message) {
      this.successTitle = title;
      this.successMessage = message;
      this.showSuccessModal = true;
    },
    
    showError(title, message) {
      this.errorTitle = title;
      this.errorMessage = message;
      this.showErrorModal = true;
    },
    
    closeModal() {
      this.showModal = false;
    },
    
    closeSuccessModal() {
      this.showSuccessModal = false;
    },
    
    closeErrorModal() {
      this.showErrorModal = false;
    },
    
    closeStudentCoursesModal() {
      this.showStudentCoursesModal = false;
      this.studentCoursesList = [];
      this.selectedStudentForCourses = null;
    },
    
    closeCourseStudentsModal() {
      this.showCourseStudentsModal = false;
      this.courseStudentsList = [];
      this.selectedCourseForStudents = null;
    },
    
    closeAllCoursesModal() {
      this.showAllCoursesModal = false;
    },

    // Open modals (added to match template usage)
    openAllCoursesModal() {
      this.showAllCoursesModal = true;
    },
    
    closeStudentsListModal() {
      this.showStudentsListModal = false;
    },

    // Open students list modal (added to match template usage)
    openStudentsListModal() {
      this.showStudentsListModal = true;
    },
    
    closeEditCourseModal() {
      this.showEditCourseModal = false;
      this.editingCourse = {
        id: null,
        title: '',
        code: '',
        credit_units: '',
        description: ''
      };
    },

    // Toast helper (used in mounted and elsewhere)
    showToast(title, message, type = 'info') {
      this.toast.show = true;
      this.toast.title = title;
      this.toast.message = message;
      this.toast.type = type;
      this.toast.icon =
        type === 'success'
          ? 'fa-solid fa-circle-check'
          : type === 'error'
          ? 'fa-solid fa-circle-exclamation'
          : 'fa-solid fa-info-circle';
      // Auto-hide after 4 seconds
      setTimeout(() => {
        this.toast.show = false;
      }, 4000);
    },
    // GenAI Study Tips Methods (keep as is)
    async getRandomStudyTip() {
      if (!this.selectedCourse) return;
      
      try {
        const response = await api.getStudyTips(
          this.selectedCourse.title,
          this.selectedCourse.credit_units
        );
        
        if (response.tips && response.tips.length > 0) {
          const randomIndex = Math.floor(Math.random() * response.tips.length);
          this.currentStudyTip = response.tips[randomIndex];
          this.currentTipIndex = randomIndex;
          this.checkIfTipSaved();
        }
      } catch (error) {
        console.error('Error getting study tips:', error);
        const fallbackTips = [
          "Break your study sessions into 25-minute focused blocks with 5-minute breaks (Pomodoro Technique).",
          "Teach the material to someone else - explaining concepts reinforces your understanding.",
          "Create mind maps to visualize connections between complex topics.",
          "Use spaced repetition - review material at increasing intervals for better retention.",
          "Study in different environments to create multiple memory associations."
        ];
        const randomIndex = Math.floor(Math.random() * fallbackTips.length);
        this.currentStudyTip = fallbackTips[randomIndex];
        this.currentTipIndex = randomIndex;
        this.checkIfTipSaved();
      }
    },
    
    nextTip() {
      this.getRandomStudyTip();
    },
    
    saveTip() {
      if (!this.savedTips.includes(this.currentStudyTip)) {
        this.savedTips.push(this.currentStudyTip);
        this.isTipSaved = true;
        localStorage.setItem('savedStudyTips', JSON.stringify(this.savedTips));
      }
    },
    
    removeTip(index) {
      this.savedTips.splice(index, 1);
      localStorage.setItem('savedStudyTips', JSON.stringify(this.savedTips));
      this.checkIfTipSaved();
    },
    
    checkIfTipSaved() {
      this.isTipSaved = this.savedTips.includes(this.currentStudyTip);
    },
    
    hideStudyTip() {
      setTimeout(() => {
        this.showStudyTip = false;
      }, 300);
    },

    // Quick Stats click handlers
    viewAllStudents() {
      this.showStudentsListModal = true;
    },
    
    viewAllCourses() {
      this.showAllCoursesModal = true;
    },
    
    viewAllEnrollments() {
      this.showSuccess('Enrollments Overview', 
        `There are currently ${this.statistics.total_enrollments} course enrollments in the system.`);
    },

    // Format date helper
    formatDate(dateString) {
      if (!dateString) return 'Recently';
      try {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
          year: 'numeric',
          month: 'short',
          day: 'numeric'
        });
      } catch (e) {
        return 'Recently';
      }
    },

    // Get enrollment date
    getEnrollmentDate(courseCode, studentId = null) {
      // This would require additional backend endpoint
      return 'Recently';
    }
  },
  
  watch: {
    'form.course'(newCourse) {
      if (newCourse) {
        this.getRandomStudyTip();
      }
    }
  },
  
  async mounted() {
  console.log('🚀 Frontend mounted, connecting to backend...');
  
  // Load saved tips from localStorage
  const savedTips = localStorage.getItem('savedStudyTips');
  if (savedTips) {
    try {
      this.savedTips = JSON.parse(savedTips);
    } catch (e) {
      this.savedTips = [];
    }
  }
  
  // Add a connection test button to navbar for debugging
  setTimeout(async () => {
    try {
      const result = await api.testConnection();
      console.log('✅ Connection test:', result);
      this.isBackendConnected = true;  // ADD THIS LINE
      this.showToast('Connected', 'Backend server is online', 'success');
    } catch (error) {
      console.error('❌ Connection test failed:', error);
      this.isBackendConnected = false;  // ADD THIS LINE
      this.showToast('Disconnected', 'Cannot connect to backend server', 'error');
    }
  }, 1000);
  
  // Load all data from backend
  await this.loadAllData();
}
}
</script>

<style scoped>

/* Enhanced Loading Indicator */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(4px);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 9999;
  font-family: 'Segoe UI', system-ui, sans-serif;
}

.loading-spinner {
  width: 60px;
  height: 60px;
  border: 4px solid rgba(59, 130, 246, 0.1);
  border-top: 4px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1.5rem;
  box-shadow: 0 0 30px rgba(59, 130, 246, 0.2);
}

.loading-text {
  color: #374151;
  font-size: 1.1rem;
  font-weight: 600;
  background: linear-gradient(90deg, #3b82f6, #8b5cf6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: pulse 2s infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

/* Connection Status Badge */
.connection-status {
  z-index: 9999;
  position: fixed;
  bottom: 20px;
  right: 20px;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 6px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.connection-status.connected {
  background: rgba(16, 185, 129, 0.15);
  color: #065f46;
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.connection-status.disconnected {
  background: rgba(239, 68, 68, 0.15);
  color: #7f1d1d;
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.connection-status i {
  font-size: 0.8rem;
}

/* Toast Notifications */
.toast-notification {
  position: fixed;
  top: 20px;
  right: 20px;
  background: white;
  padding: 1rem 1.5rem;
  border-radius: 0.75rem;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
  border-left: 4px solid #3b82f6;
  z-index: 999;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  animation: slideIn 0.3s ease-out;
  max-width: 350px;
}

.toast-notification.success {
  border-left-color: #10b981;
}

.toast-notification.error {
  border-left-color: #ef4444;
}

.toast-notification.info {
  border-left-color: #3b82f6;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(100%);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* Base Styles */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

#app {
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  min-height: 100vh;
  color: #333;
  line-height: 1.6;
}

.container {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 1rem;
}

/* Navigation Bar */
.navbar {
  background: white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-brand {
  font-size: 1.5rem;
  font-weight: 700;
  color: #2d3748;
}

.nav-brand i {
  color: #3b82f6;
  margin-right: 0.5rem;
}

.nav-button {
  background: #3b82f6;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 4px 10px rgba(59, 130, 246, 0.3);
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1rem;
}

.nav-button:hover {
  background: #2563eb;
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(59, 130, 246, 0.4);
}

.nav-button i {
  color: white !important;
  font-size: 1.1rem;
  filter: brightness(0) invert(1);
}

/* Main Content */
.main-content {
  padding: 2rem 0;
}

/* Card Styles */
.card {
  background: white;
  border-radius: 1rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  padding: 2rem;
  margin-bottom: 2rem;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.12);
}

/* Section Headings */
.section-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #2d3748;
  margin-bottom: 1.5rem;
}

.section-title-center {
  text-align: center;
}

/* Course Management Styles */
.course-management-container {
  max-width: 100%;
}

.management-actions {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.management-actions .btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.management-actions .btn-outline {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.create-course-form {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  animation: slideDown 0.3s ease-out;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}

.form-textarea {
  width: 100%;
  padding: 0.875rem;
  border: 1px solid #cbd5e0;
  border-radius: 0.5rem;
  background: white;
  font-size: 1rem;
  resize: vertical;
  min-height: 80px;
  max-height: 150px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  transition: border-color 0.3s, box-shadow 0.3s;
}

.form-textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
}

.form-hint {
  display: block;
  color: #64748b;
  font-size: 0.8rem;
  margin-top: 0.25rem;
}

.form-actions {
  margin-top: 1.5rem;
}

/* Recent Courses Styles */
.recent-courses {
  margin-top: 2rem;
}

.sub-section-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #4a5568;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.recent-courses-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.recent-course-card {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  padding: 1.25rem;
  transition: all 0.3s ease;
}

.recent-course-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  border-color: #cbd5e0;
}

.recent-course-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.75rem;
}

.recent-course-header h4 {
  font-size: 1rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
  flex: 1;
}

.course-code-small {
  background: #3b82f6;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 0.5rem;
  font-size: 0.75rem;
  font-weight: 500;
  margin-left: 0.5rem;
}

.recent-course-body {
  margin-bottom: 0.75rem;
}

.course-description-small {
  color: #64748b;
  font-size: 0.85rem;
  line-height: 1.4;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.recent-course-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.8rem;
  color: #94a3b8;
}

.credit-units-small {
  background: #dbeafe;
  color: #1e40af;
  padding: 0.2rem 0.6rem;
  border-radius: 1rem;
  font-weight: 500;
}

.course-date {
  font-size: 0.75rem;
}

/* Home Section */
.home-description {
  color: #4a5568;
  margin-bottom: 2rem;
  line-height: 1.7;
  font-size: 1.1rem;
  text-align: center;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}

.columns {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

@media (max-width: 768px) {
  .columns {
    grid-template-columns: 1fr;
  }

  .navbar {
    padding: 1rem;
  }

  .nav-brand {
    font-size: 1.2rem;
  }

  .nav-button {
    padding: 0.6rem 1rem;
    font-size: 0.9rem;
  }

  .management-actions {
    flex-direction: column;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .recent-courses-grid {
    grid-template-columns: 1fr;
  }
}

.column-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #4a5568;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
}

.column-title i {
  color: #3b82f6;
  margin-right: 0.5rem;
}

/* Form Styles */
.form-container {
  max-width: 100%;
}

.form-group {
  margin-bottom: 1.5rem;
  position: relative;
}

.form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.form-label {
  color: #4a5568;
  font-weight: 500;
}

.form-input {
  width: 100%;
  padding: 0.875rem;
  border: 1px solid #cbd5e0;
  border-radius: 0.5rem;
  background: white;
  font-size: 1rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  transition: border-color 0.3s, box-shadow 0.3s;
}

.form-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
}

/* Divider */
.divider {
  height: 1px;
  background: linear-gradient(to right, transparent, #e2e8f0, transparent);
  margin: 2rem 0;
}

/* Button Styles */
.btn {
  background: #3b82f6;
  color: white;
  border: none;
  padding: 0.75rem 2rem;
  border-radius: 0.5rem;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.btn:hover {
  background: #2563eb;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
}

.btn:disabled {
  background: #cbd5e0;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.btn-full {
  width: 100%;
  padding: 0.875rem;
  margin-top: 1rem;
}

/* Outline Button */
.btn-outline {
  background: transparent;
  color: #3b82f6;
  border: 2px solid #3b82f6;
  padding: 0.75rem 2rem;
  border-radius: 0.5rem;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.btn-outline:hover {
  background: #3b82f6;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(59, 130, 246, 0.3);
}

/* Enroll Form Styles */
.enroll-form-container {
  max-width: 28rem;
  margin: 0 auto;
}

.select-wrapper {
  position: relative;
}

.form-select {
  width: 100%;
  padding: 0.875rem;
  border: 1px solid #cbd5e0;
  border-radius: 0.5rem;
  background: white;
  appearance: none;
  font-size: 1rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  transition: border-color 0.3s, box-shadow 0.3s;
}

.form-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
}

.select-arrow {
  position: absolute;
  right: 0.875rem;
  top: 50%;
  transform: translateY(-50%);
  color: #4a5568;
  pointer-events: none;
}

/* Students List Modal Styles */
.students-table-container {
  margin: 1.5rem 0;
  max-height: 400px;
  overflow-y: auto;
  border-radius: 0.5rem;
  border: 1px solid #e2e8f0;
}

.students-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
}

.students-table thead {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  position: sticky;
  top: 0;
  z-index: 10;
}

.students-table th {
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.students-table td {
  padding: 1rem;
  border-bottom: 1px solid #e2e8f0;
}

.student-row {
  transition: all 0.3s ease;
}

.student-row:hover {
  background: #f8fafc;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.student-id {
  font-weight: 600;
  color: #3b82f6;
  font-family: 'Courier New', monospace;
}

.student-name {
  font-weight: 600;
  color: #2d3748;
}

.student-name-wrapper {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.student-icon {
  color: #3b82f6;
  font-size: 0.9rem;
}

.student-email {
  color: #64748b;
  font-size: 0.9rem;
}

.student-actions {
  text-align: right;
}

.view-courses-btn {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-size: 0.85rem;
  font-weight: 500;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
  box-shadow: 0 2px 5px rgba(59, 130, 246, 0.2);
}

.view-courses-btn:hover {
  background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 10px rgba(59, 130, 246, 0.3);
}

.view-courses-btn i {
  font-size: 0.8rem;
}

.modal-footer {
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.total-students,
.total-courses {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #64748b;
  font-weight: 500;
}

.total-students i,
.total-courses i {
  color: #3b82f6;
}

.close-btn {
  padding: 0.5rem 1.5rem;
  font-size: 0.9rem;
}

/* GenAI Study Tips Floating Card */
.study-tips-floating {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border-radius: 0.75rem;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
  border: 1px solid #e2e8f0;
  z-index: 10;
  margin-top: 0.5rem;
  animation: slideDown 0.3s ease-out;
}

.floating-header {
  display: flex;
  align-items: center;
  padding: 1rem 1.25rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 0.75rem 0.75rem 0 0;
}

.floating-header i {
  margin-right: 0.5rem;
  font-size: 1.1rem;
}

.floating-header h4 {
  margin: 0;
  flex: 1;
  font-size: 1rem;
  font-weight: 600;
}

.close-tip {
  background: none;
  border: none;
  color: white;
  font-size: 1.25rem;
  cursor: pointer;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.floating-content {
  padding: 1.25rem;
}

.floating-content p {
  margin: 0 0 1rem 0;
  color: #4a5568;
  line-height: 1.5;
}

.tip-actions {
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
}

.tip-btn {
  background: #3b82f6;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-size: 0.85rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  transition: all 0.3s ease;
}

.tip-btn:hover {
  background: #2563eb;
  transform: translateY(-1px);
}

.tip-btn.saved {
  background: #10b981;
  cursor: default;
}

.tip-btn.saved:hover {
  background: #10b981;
  transform: none;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Saved Study Tips Section */
.saved-tips-section {
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
}

.saved-tips-header {
  display: flex;
  align-items: center;
  margin-bottom: 0.75rem;
}

.saved-tips-header i {
  color: #f59e0b;
  margin-right: 0.5rem;
}

.saved-tips-header h5 {
  margin: 0;
  color: #374151;
  font-size: 0.95rem;
}

.saved-tips-list {
  max-height: 150px;
  overflow-y: auto;
}

.saved-tip-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  padding: 0.75rem;
  margin-bottom: 0.5rem;
}

.saved-tip-item p {
  margin: 0;
  flex: 1;
  color: #4a5568;
  font-size: 0.85rem;
  line-height: 1.4;
}

.remove-tip {
  background: none;
  border: none;
  color: #ef4444;
  cursor: pointer;
  padding: 0.25rem;
  margin-left: 0.5rem;
  border-radius: 0.25rem;
  transition: background 0.3s ease;
}

.remove-tip:hover {
  background: #fef2f2;
}

/* Course Preview Styles */
.course-preview {
  margin-top: 1rem;
}

.preview-card {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  padding: 1.25rem;
  transition: all 0.3s ease;
}

.preview-card:hover {
  background: #f1f5f9;
  border-color: #cbd5e0;
}

.preview-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 0.75rem;
}

.preview-details {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.course-code {
  background: #3b82f6;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.875rem;
  font-weight: 500;
}

.credit-units {
  color: #64748b;
  font-size: 0.875rem;
  font-weight: 500;
}

.course-description {
  color: #475569;
  font-size: 0.9rem;
  line-height: 1.5;
  margin: 0;
}

/* Stats Card Styles */
.stats-card {
  text-align: center;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  margin-top: 1rem;
}

.stat-item {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 1rem;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.stat-item:hover {
  background: #f1f5f9;
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  font-size: 2.5rem;
  color: #3b82f6;
  margin-bottom: 1rem;
}

.stat-info h3 {
  font-size: 2rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.stat-info p {
  color: #64748b;
  font-size: 0.9rem;
  margin: 0;
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }

  .students-table {
    font-size: 0.85rem;
  }

  .students-table th,
  .students-table td {
    padding: 0.75rem;
  }
}

/* Modal Styles */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1000;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1rem;
}

.modal-content {
  background: white;
  border-radius: 1rem;
  padding: 2rem;
  max-width: 800px;
  width: 100%;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  position: relative;
}

.close-modal {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #4a5568;
  transition: color 0.3s;
}

.close-modal:hover {
  color: #2d3748;
}

.modal-header {
  display: flex;
  align-items: center;
  margin-bottom: 1.5rem;
  gap: 1rem;
}

.modal-header-icon {
  font-size: 2rem;
  color: #f59e0b;
}

.study-tips-list {
  list-style: none;
  margin-bottom: 1.5rem;
}

.study-tip {
  display: flex;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.bullet-point {
  display: inline-block;
  width: 6px;
  height: 6px;
  background-color: #3b82f6;
  border-radius: 50%;
  margin-right: 0.75rem;
  margin-top: 0.5rem;
  flex-shrink: 0;
}

.tip-box {
  background: #dbeafe;
  border: 1px solid #bfdbfe;
  border-radius: 0.5rem;
  padding: 1rem;
  margin-top: 1.5rem;
}

.tip-header {
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;
}

.tip-icon {
  color: #3b82f6;
  font-size: 1.25rem;
  margin-right: 0.75rem;
}

.tip-title {
  font-weight: 600;
  color: #1e40af;
}

.tip-content {
  color: #1e40af;
}

/* Success Modal Styles */
.success-modal {
  text-align: center;
  max-width: 500px;
  padding: 3rem 2rem;
}

.success-icon {
  font-size: 4rem;
  color: #10b981;
  margin-bottom: 1.5rem;
  animation: bounce 0.6s ease-in-out;
}

.success-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #065f46;
  margin-bottom: 1rem;
}

.success-message {
  color: #047857;
  font-size: 1.1rem;
  line-height: 1.6;
  margin-bottom: 2rem;
}

.success-btn {
  background: #10b981 !important;
  padding: 0.75rem 2rem;
  border-radius: 0.5rem;
  font-size: 1rem;
}

.success-btn:hover {
  background: #059669 !important;
  transform: translateY(-2px);
}

/* Error Modal Styles */
.error-modal {
  text-align: center;
  max-width: 500px;
  padding: 3rem 2rem;
}

.error-icon {
  font-size: 4rem;
  color: #ef4444;
  margin-bottom: 1.5rem;
  animation: shake 0.5s ease-in-out;
}

.error-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #7f1d1d;
  margin-bottom: 1rem;
}

.error-message {
  color: #b91c1c;
  font-size: 1.1rem;
  line-height: 1.6;
  margin-bottom: 2rem;
}

.error-btn {
  background: #ef4444 !important;
  padding: 0.75rem 2rem;
  border-radius: 0.5rem;
  font-size: 1rem;
}

.error-btn:hover {
  background: #dc2626 !important;
  transform: translateY(-2px);
}

/* List Modal Styles */
.list-modal {
  max-width: 800px;
  max-height: 70vh;
}

.list-container {
  max-height: 400px;
  overflow-y: auto;
}

.list-item {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  padding: 1.25rem;
  margin-bottom: 1rem;
  transition: all 0.3s ease;
}

.list-item:hover {
  background: #f1f5f9;
  border-color: #cbd5e0;
}

.list-item-main {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.75rem;
}

.course-info {
  flex: 1;
}

.course-info h4 {
  font-size: 1.1rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.course-actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

/* View-students-btn styles */
.view-students-btn {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-size: 0.85rem;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  transition: all 0.3s ease;
  font-weight: 500;
  box-shadow: 0 2px 5px rgba(16, 185, 129, 0.2);
}

.view-students-btn:hover {
  background: linear-gradient(135deg, #059669 0%, #047857 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 10px rgba(16, 185, 129, 0.3);
}

.edit-course-btn {
  background: #3b82f6;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-size: 0.85rem;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  transition: all 0.3s ease;
}

.edit-course-btn:hover {
  background: #2563eb;
  transform: translateY(-1px);
  box-shadow: 0 2px 5px rgba(59, 130, 246, 0.3);
}

.delete-course-btn {
  background: #ef4444;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-size: 0.85rem;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  transition: all 0.3s ease;
}

.delete-course-btn:hover {
  background: #dc2626;
  transform: translateY(-1px);
  box-shadow: 0 2px 5px rgba(239, 68, 68, 0.3);
}

.student-email, .course-code {
  color: #ffffff;
  font-size: 0.9rem;
}

.course-description-modal {
  margin-top: 0.75rem;
  padding-top: 0.75rem;
  border-top: 1px dashed #e2e8f0;
}

.course-description-modal p {
  color: #64748b;
  font-size: 0.9rem;
  line-height: 1.5;
  margin: 0;
}

.list-item-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 0.75rem;
  font-size: 0.85rem;
  color: #94a3b8;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.enrollment-date, .course-count, .student-count, .course-date {
  font-size: 0.8rem;
}

.empty-state {
  text-align: center;
  padding: 3rem 2rem;
  color: #94a3b8;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  color: #cbd5e0;
}

@keyframes bounce {
  0%, 20%, 60%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-10px);
  }
  80% {
    transform: translateY(-5px);
  }
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-5px); }
  75% { transform: translateX(5px); }
}

/* Footer */
.footer {
  text-align: center;
  padding: 2rem 0;
  color: #6b7280;
  font-size: 0.9rem;
}
</style>
