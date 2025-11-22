<template>
  <div id="app">
    <!-- Navigation Bar -->
    <nav class="navbar">
      <div class="nav-brand">
        <i class="fas fa-graduation-cap"></i> Course Enrollment System
      </div>
      <button class="nav-button" @click="showModal = true">
        <i class="fas fa-lightbulb"></i> Study Tips
      </button>
    </nav>

    <!-- Main Content -->
    <div class="container">
      <div class="main-content">
        <!-- Home Section -->
        <section class="card">
          <h2 class="section-title">Home</h2>
          <p class="home-description">
            Your journey begins here! <br> Register students and manage courses with ease. Let's transform education together.</br>
          </p>
          
          <div class="form-container">
            <div class="columns">
              <!-- Name Column -->
              <div>
                <h3 class="column-title">
                  <i class="fas fa-user"></i> Name
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
                  <i class="fas fa-book"></i> Course
                </h3>
                <div class="form-group">
                  <div class="select-wrapper">
                    <select class="form-select" v-model="form.course">
                      <option value="">Choose a course...</option>
                      <option v-for="course in courses" :key="course.code" :value="course.code">
                        {{ course.code }} - {{ course.title }} ({{ course.credit_units }} CU)
                      </option>
                    </select>
                    <div class="select-arrow">
                      <i class="fas fa-chevron-down"></i>
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
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Register Button -->
            <button class="btn btn-full" @click="registerStudent">Register Student</button>
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
                <button class="info-btn" @click="viewStudentCourses" title="View student's courses">
                  <i class="fas fa-list"></i>
                </button>
              </div>
              <div class="select-wrapper">
                <select class="form-select" v-model="enrollment.student">
                  <option value="">Choose a student...</option>
                  <option v-for="student in availableStudents" :key="student.id" :value="student.id">
                    {{ student.name }} ({{ student.email }})
                  </option>
                </select>
                <div class="select-arrow">
                  <i class="fas fa-chevron-down"></i>
                </div>
              </div>
            </div>
            
            <!-- Select Course -->
            <div class="form-group">
              <div class="form-header">
                <label class="form-label">Select Course</label>
                <button class="info-btn" @click="viewCourseStudents" title="View enrolled students">
                  <i class="fas fa-users"></i>
                </button>
              </div>
              <div class="select-wrapper">
                <select class="form-select" v-model="enrollment.course">
                  <option value="">Choose a course...</option>
                  <option v-for="course in availableCourses" :key="course.code" :value="course.code">
                    {{ course.code }} - {{ course.title }} ({{ course.credit_units }} CU)
                  </option>
                </select>
                <div class="select-arrow">
                  <i class="fas fa-chevron-down"></i>
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
                <i class="fas fa-user-graduate"></i>
              </div>
              <div class="stat-info">
                <h3>{{ allStudents.length }}</h3>
                <p>Registered Students</p>
              </div>
            </div>
            <div class="stat-item" @click="viewAllCourses">
              <div class="stat-icon">
                <i class="fas fa-book-open"></i>
              </div>
              <div class="stat-info">
                <h3>{{ courses.length }}</h3>
                <p>Available Courses</p>
              </div>
            </div>
            <div class="stat-item" @click="viewAllEnrollments">
              <div class="stat-icon">
                <i class="fas fa-clipboard-list"></i>
              </div>
              <div class="stat-info">
                <h3>{{ totalEnrollments }}</h3>
                <p>Total Enrollments</p>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>

    <!-- Footer -->
    <div class="footer">
      <p>Course Enrollment System &copy; 2025. All rights reserved.</p>
    </div>

    <!-- Study Tips Modal -->
    <div class="modal" v-if="showModal" @click="closeModal">
      <div class="modal-content" @click.stop>
        <button class="close-modal" @click="showModal = false">&times;</button>
        <div class="modal-header">
          <i class="fas fa-lightbulb modal-header-icon"></i>
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
            <i class="fas fa-graduation-cap tip-icon"></i>
            <h3 class="tip-title">Effective Study Environment</h3>
          </div>
          <p class="tip-content">Choose a quiet, well-lit space dedicated to studying. Keep your study area organized and free from distractions like phones and social media. Natural light and proper ergonomics can significantly improve focus and productivity.</p>
        </div>
        
        <div class="tip-box">
          <div class="tip-header">
            <i class="fas fa-brain tip-icon"></i>
            <h3 class="tip-title">Memory Enhancement Techniques</h3>
          </div>
          <p class="tip-content">Use mnemonic devices, create associations with existing knowledge, and practice retrieval through flashcards. Sleep plays a crucial role in memory consolidation, so ensure you get 7-9 hours of quality sleep during intensive study periods.</p>
        </div>

        <div class="tip-box">
          <div class="tip-header">
            <i class="fas fa-clock tip-icon"></i>
            <h3 class="tip-title">Time Management</h3>
          </div>
          <p class="tip-content">Create a weekly study schedule that allocates specific time blocks for each subject. Prioritize difficult topics when your energy levels are highest, and include regular review sessions to reinforce learning.</p>
        </div>

        <div class="tip-box">
          <div class="tip-header">
            <i class="fas fa-heart tip-icon"></i>
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
          <i class="fas fa-check-circle"></i>
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
          <i class="fas fa-exclamation-circle"></i>
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
          <i class="fas fa-user-graduate modal-header-icon"></i>
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
          <i class="fas fa-book-open empty-icon"></i>
          <p>No courses enrolled yet</p>
        </div>
      </div>
    </div>

    <!-- Course Students Modal -->
    <div class="modal" v-if="showCourseStudentsModal" @click="closeCourseStudentsModal">
      <div class="modal-content list-modal" @click.stop>
        <button class="close-modal" @click="closeCourseStudentsModal">&times;</button>
        <div class="modal-header">
          <i class="fas fa-users modal-header-icon"></i>
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
          <i class="fas fa-user-slash empty-icon"></i>
          <p>No students enrolled yet</p>
        </div>
      </div>
    </div>

    <!-- All Students Modal -->
    <div class="modal" v-if="showAllStudentsModal" @click="closeAllStudentsModal">
      <div class="modal-content list-modal" @click.stop>
        <button class="close-modal" @click="closeAllStudentsModal">&times;</button>
        <div class="modal-header">
          <i class="fas fa-user-graduate modal-header-icon"></i>
          <h2 class="section-title">All Registered Students</h2>
        </div>
        
        <div v-if="allStudents.length > 0" class="list-container">
          <div v-for="student in allStudents" :key="student.id" class="list-item">
            <div class="list-item-main">
              <h4>{{ student.name }}</h4>
              <span class="student-email">{{ student.email }}</span>
            </div>
            <div class="list-item-meta">
              <span class="course-count">{{ getStudentCourseCount(student.id) }} courses</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- All Courses Modal -->
    <div class="modal" v-if="showAllCoursesModal" @click="closeAllCoursesModal">
      <div class="modal-content list-modal" @click.stop>
        <button class="close-modal" @click="closeAllCoursesModal">&times;</button>
        <div class="modal-header">
          <i class="fas fa-book-open modal-header-icon"></i>
          <h2 class="section-title">All Available Courses</h2>
        </div>
        
        <div class="list-container">
          <div v-for="course in courses" :key="course.code" class="list-item">
            <div class="list-item-main">
              <h4>{{ course.title }}</h4>
              <span class="course-code">{{ course.code }}</span>
            </div>
            <div class="list-item-meta">
              <span class="credit-units">{{ course.credit_units }} CU</span>
              <span class="student-count">{{ getCourseStudentCount(course.code) }} students</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      showModal: false,
      showSuccessModal: false,
      showErrorModal: false,
      showStudentCoursesModal: false,
      showCourseStudentsModal: false,
      showAllStudentsModal: false,
      showAllCoursesModal: false,
      successTitle: '',
      successMessage: '',
      errorTitle: '',
      errorMessage: '',
      form: {
        name: '',
        email: '',
        course: ''
      },
      enrollment: {
        student: '',
        course: ''
      },
      // Track registered students to prevent duplicates
      registeredStudents: [],
      // Lists for modals
      studentCoursesList: [],
      courseStudentsList: [],
      selectedStudentForCourses: null,
      selectedCourseForStudents: null,
      // Initial sample students (for enrollment dropdown)
      initialStudents: [
        { id: 1, name: 'John Student', email: 'john@student.com' },
        { id: 2, name: 'Phebe Student', email: 'phebe@student.com' },
        { id: 3, name: 'Zoe Smith', email: 'zoe.smith@student.com' },
        { id: 4, name: 'Emily Johnson', email: 'emily.johnson@student.com' }
      ],
      courses: [
        { 
          code: 'CS101', 
          title: 'Introduction to Computer Science', 
          credit_units: 3,
          description: 'Fundamental concepts of computer science, algorithms, and programming principles.'
        },
        { 
          code: 'WD201', 
          title: 'Web Development Fundamentals', 
          credit_units: 4,
          description: 'Comprehensive course covering HTML, CSS, JavaScript and modern web development practices.'
        },
        { 
          code: 'DS301', 
          title: 'Data Science Essentials', 
          credit_units: 4,
          description: 'Introduction to data analysis, visualization, and machine learning concepts.'
        },
        { 
          code: 'UX401', 
          title: 'UI/UX Design Principles', 
          credit_units: 3,
          description: 'User interface and experience design methodologies and best practices.'
        },
        { 
          code: 'DM501', 
          title: 'Digital Marketing Strategies', 
          credit_units: 3,
          description: 'Modern digital marketing techniques including SEO, social media, and content marketing.'
        },
        { 
          code: 'MA601', 
          title: 'Mobile App Development', 
          credit_units: 4,
          description: 'Cross-platform mobile application development using modern frameworks and tools.'
        }
      ]
    }
  },
  computed: {
    selectedCourse() {
      return this.courses.find(course => course.code === this.form.course);
    },
    enrolledCourse() {
      return this.courses.find(course => course.code === this.enrollment.course);
    },
    // Combine initial students with newly registered ones
    allStudents() {
      return [...this.initialStudents, ...this.registeredStudents];
    },
    // Students available for enrollment (only registered ones)
    availableStudents() {
      return this.allStudents;
    },
    // Courses available for enrollment
    availableCourses() {
      return this.courses;
    },
    // Total enrollments count
    totalEnrollments() {
      const enrollments = JSON.parse(localStorage.getItem('courseEnrollments') || '{}');
      return Object.keys(enrollments).length;
    }
  },
  methods: {
    registerStudent() {
      if (this.form.name && this.form.email && this.form.course) {
        // Check if student is already registered
        const isAlreadyRegistered = this.registeredStudents.some(
          student => student.email.toLowerCase() === this.form.email.toLowerCase()
        );
        
        if (isAlreadyRegistered) {
          this.showError('Registration Failed', 'This email is already registered. Please use a different email address.');
          return;
        }

        const selectedCourse = this.courses.find(c => c.code === this.form.course);
        
        // Generate a unique ID for the new student
        const newStudentId = this.allStudents.length + 1;
        
        // Add to registered students
        this.registeredStudents.push({
          id: newStudentId,
          name: this.form.name,
          email: this.form.email
        });
        
        // Show success modal
        this.showSuccess('Registration Successful!', 
          `Congratulations ${this.form.name}, your registration for ${selectedCourse.code} - ${selectedCourse.title} has been completed successfully!`);
        
        // Reset form
        this.form = { name: '', email: '', course: '' };
      } else {
        this.showError('Incomplete Form', 'Please fill in all fields to complete registration.');
      }
    },
    enrollStudent() {
      if (this.enrollment.student && this.enrollment.course) {
        const student = this.allStudents.find(s => s.id === this.enrollment.student);
        const course = this.courses.find(c => c.code === this.enrollment.course);
        
        // Check if student is already enrolled in this course
        const enrollmentKey = `${student.id}-${course.code}`;
        const enrollments = JSON.parse(localStorage.getItem('courseEnrollments') || '{}');
        
        if (enrollments[enrollmentKey]) {
          this.showError('Enrollment Failed', `${student.name} is already enrolled in ${course.code} - ${course.title}.`);
          return;
        }
        
        // Record enrollment
        enrollments[enrollmentKey] = {
          studentId: student.id,
          studentName: student.name,
          courseCode: course.code,
          courseTitle: course.title,
          enrolledAt: new Date().toISOString()
        };
        localStorage.setItem('courseEnrollments', JSON.stringify(enrollments));
        
        // Show success modal
        this.showSuccess('Enrollment Successful!', 
          `Congratulations ${student.name}, you have been successfully enrolled in ${course.code} - ${course.title}! Your academic journey begins now.`);
        
        // Reset enrollment
        this.enrollment = { student: '', course: '' };
      } else {
        this.showError('Incomplete Selection', 'Please select both student and course to complete enrollment.');
      }
    },
    // View student's courses
    viewStudentCourses() {
      if (!this.enrollment.student) {
        this.showError('No Student Selected', 'Please select a student to view their courses.');
        return;
      }
      
      const student = this.allStudents.find(s => s.id === this.enrollment.student);
      const enrollments = JSON.parse(localStorage.getItem('courseEnrollments') || '{}');
      
      // Get courses for this student
      this.studentCoursesList = Object.values(enrollments)
        .filter(enrollment => enrollment.studentId === student.id)
        .map(enrollment => {
          const course = this.courses.find(c => c.code === enrollment.courseCode);
          return {
            ...course,
            enrolledAt: enrollment.enrolledAt
          };
        });
      
      this.selectedStudentForCourses = student;
      this.showStudentCoursesModal = true;
    },
    // View students in a course
    viewCourseStudents() {
      if (!this.enrollment.course) {
        this.showError('No Course Selected', 'Please select a course to view enrolled students.');
        return;
      }
      
      const course = this.courses.find(c => c.code === this.enrollment.course);
      const enrollments = JSON.parse(localStorage.getItem('courseEnrollments') || '{}');
      
      // Get students for this course
      this.courseStudentsList = Object.values(enrollments)
        .filter(enrollment => enrollment.courseCode === course.code)
        .map(enrollment => {
          const student = this.allStudents.find(s => s.id === enrollment.studentId);
          return {
            ...student,
            enrolledAt: enrollment.enrolledAt
          };
        });
      
      this.selectedCourseForStudents = course;
      this.showCourseStudentsModal = true;
    },
    // View all students
    viewAllStudents() {
      this.showAllStudentsModal = true;
    },
    // View all courses
    viewAllCourses() {
      this.showAllCoursesModal = true;
    },
    // View all enrollments
    viewAllEnrollments() {
      // For now, just show a message since we don't have a dedicated enrollments modal
      const enrollments = JSON.parse(localStorage.getItem('courseEnrollments') || '{}');
      this.showSuccess('Enrollments Overview', `There are currently ${Object.keys(enrollments).length} course enrollments in the system.`);
    },
    // Helper methods
    getEnrollmentDate(courseCode, studentId = null) {
      const enrollments = JSON.parse(localStorage.getItem('courseEnrollments') || '{}');
      let enrollmentKey;
      
      if (studentId) {
        enrollmentKey = `${studentId}-${courseCode}`;
      } else {
        // For student courses view
        enrollmentKey = `${this.selectedStudentForCourses.id}-${courseCode}`;
      }
      
      const enrollment = enrollments[enrollmentKey];
      if (enrollment && enrollment.enrolledAt) {
        return new Date(enrollment.enrolledAt).toLocaleDateString();
      }
      return 'Unknown';
    },
    getStudentCourseCount(studentId) {
      const enrollments = JSON.parse(localStorage.getItem('courseEnrollments') || '{}');
      return Object.values(enrollments).filter(e => e.studentId === studentId).length;
    },
    getCourseStudentCount(courseCode) {
      const enrollments = JSON.parse(localStorage.getItem('courseEnrollments') || '{}');
      return Object.values(enrollments).filter(e => e.courseCode === courseCode).length;
    },
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
    closeAllStudentsModal() {
      this.showAllStudentsModal = false;
    },
    closeAllCoursesModal() {
      this.showAllCoursesModal = false;
    }
  },
  mounted() {
    // Add interactive functionality
    const formElements = document.querySelectorAll('.form-select, .form-input');
    
    formElements.forEach(element => {
      element.addEventListener('focus', function() {
        this.style.boxShadow = '0 0 0 3px rgba(59, 130, 246, 0.2)';
      });
      
      element.addEventListener('blur', function() {
        this.style.boxShadow = '';
      });
    });
  }
}
</script>

<style scoped>
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

.info-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.info-btn:hover {
  background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
  transform: scale(1.1);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
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
}

.btn:hover {
  background: #2563eb;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
}

.btn-full {
  width: 100%;
  padding: 0.875rem;
  margin-top: 1rem;
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
}

/* Study Tips Modal */
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
  max-width: 600px;
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
  max-width: 600px;
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

.list-item-main h4 {
  font-size: 1.1rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.student-email, .course-code {
  color: #d7dce2;
  font-size: 0.9rem;
}

.list-item-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 0.75rem;
  font-size: 0.85rem;
  color: #94a3b8;
}

.enrollment-date, .course-count, .student-count {
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
