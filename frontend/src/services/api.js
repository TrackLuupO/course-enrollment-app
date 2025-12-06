// API Service for connecting Vue frontend with FastAPI backend
const API_BASE_URL = '/api';  // Changed to use proxy for development (avoids direct CORS issues)

class ApiService {
    constructor() {
        this.baseUrl = API_BASE_URL;
    }

    // Helper method for making requests
    async request(endpoint, method = 'GET', data = null) {
        const url = `${this.baseUrl}${endpoint}`;
        
        console.log(`API Request: ${method} ${url}`);
        
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
            mode: 'cors', // Important for CORS
            credentials: 'same-origin', // Or 'include' if you need cookies
        };

        if (data) {
            options.body = JSON.stringify(data);
        }

        try {
            const response = await fetch(url, options);
            
            console.log(`API Response Status: ${response.status} ${response.statusText}`);
            
            // For DELETE requests that might not return content
            if (response.status === 204) {
                return { success: true };
            }
            
            if (!response.ok) {
                let errorMessage = `HTTP ${response.status}: ${response.statusText}`;
                try {
                    const errorData = await response.json();
                    errorMessage = errorData.detail || errorData.message || errorMessage;
                } catch (e) {
                    // If response is not JSON, try to get text
                    try {
                        const text = await response.text();
                        if (text) errorMessage = text;
                    } catch (e2) {
                        // Ignore
                    }
                }
                throw new Error(errorMessage);
            }

            // Try to parse JSON
            try {
                const jsonData = await response.json();
                return jsonData;
            } catch (e) {
                // If no JSON content but request was successful
                return { success: true };
            }
        } catch (error) {
            console.error('API Request Error:', error);
            
            // More specific error messages
            if (error.message.includes('Failed to fetch')) {
                throw new Error(`Cannot connect to backend server. Make sure it's running on http://localhost:8000`);
            }
            if (error.message.includes('NetworkError')) {
                throw new Error('Network error. Check your internet connection or CORS settings.');
            }
            if (error.message.includes('CORS')) {
                throw new Error('CORS error. Backend might not be configured to accept requests from this origin.');
            }
            
            throw error;
        }
    }

    // Test connection
    async testConnection() {
        try {
            console.log('Testing backend connection...');
            const health = await this.request('/health');
            console.log('Health check passed:', health);
            return { success: true, message: 'Backend is reachable' };
        } catch (error) {
            console.error('Backend connection test failed:', error);
            return { success: false, message: error.message };
        }
    }

    // Student endpoints
    async getStudents() {
        return this.request('/students/');
    }

    async createStudent(studentData) {
        return this.request('/students/', 'POST', studentData);
    }

    async getStudent(studentId) {
        return this.request(`/students/${studentId}`);
    }

    // Course endpoints
    async getCourses() {
        return this.request('/courses/');
    }

    async createCourse(courseData) {
        return this.request('/courses/', 'POST', courseData);
    }

    async updateCourse(courseId, courseData) {
        return this.request(`/courses/${courseId}`, 'PUT', courseData);
    }

    async deleteCourse(courseId) {
        return this.request(`/courses/${courseId}`, 'DELETE');
    }

    async getCourse(courseId) {
        return this.request(`/courses/${courseId}`);
    }

    // Enrollment endpoints
    async createEnrollment(enrollmentData) {
        return this.request('/enrollments/', 'POST', enrollmentData);
    }

    async getEnrollments() {
        return this.request('/enrollments/');
    }

    async getStudentEnrollments(studentId) {
        return this.request(`/enrollments/student/${studentId}`);
    }

    async getCourseEnrollments(courseId) {
        return this.request(`/enrollments/course/${courseId}`);
    }

    // Statistics
    async getStatistics() {
        return this.request('/stats/');
    }

    // Study Tips (GenAI)
    async getStudyTips(courseTitle, creditUnits) {
        return this.request('/genai/study-tips', 'POST', {
            course_title: courseTitle,
            credit_units: creditUnits
        });
    }
    // Add this method to the ApiService class in api.js:
    async checkHealth() {
    try {
    const response = await fetch(`${this.baseUrl}/health`, {
        method: 'GET',
        headers: {
        'Content-Type': 'application/json',
        },
      // Shorter timeout for health check
        signal: AbortSignal.timeout(3000)
    });

    if (response.ok) {
        const data = await response.json();
        return { success: true, data };
    }
    return { success: false, message: `HTTP ${response.status}` };
    } catch (error) {
    return {
        success: false,
        message: error.message || 'Cannot connect to backend'
    };
}
}
}

// Create singleton instance
export const api = new ApiService();