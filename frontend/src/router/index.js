import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'user_login',
      component: () => import('../views/UserLogin.vue')
    },
    {
      path : '/admin_dashboard',
      name : 'admin_dashboard',
      component : () => import('../views/AdminDashboard.vue')
    },
    {
      path : '/register',
      name : 'register',
      component : () => import('../views/RegistrationForm.vue')
    },
    {
      path : '/student_dashboard',
      name : 'student_dashboard',
      component : () => import('../views/StudentDashboard.vue')
    },
    {
      path : '/company_dashboard',
      name : 'company_dashboard',
      component : () => import('../views/CompanyDashboard.vue')
    },
    {
      path : '/edit_profile',
      name : 'edit_profile_page',
      component : () => import('../views/edit_profile.vue')
    },
    {
      path : '/company/:company_id/drives',
      component : () => import('../views/CompanyDrives.vue')
    },
    {
      path : '/apply/:placement_id/:company_id',
      component : () => import('../views/Apply.vue')
    },
    {
      path : '/application_history',
      component : () => import('../views/ApplicationHistory.vue')
    },
    {
      path : '/get_applications/:drive_id',
      component : () => import('../views/StudentApplications.vue')
    },
    {
      path : '/review_application/:drive_id/:student_id',
      component : () => import('../views/ReviewApplication.vue')
    },
    {
      path : '/ongoing_drives_admin',
      component : () => import('../views/OngoingDrivesAdmin.vue')
    },
    {
      path : '/student_applications',
      component : () => import('../views/StudentApplicationsAdmin.vue')
    },
    {
      path : '/view/:student_id/:drive_id',
      component : () => import('../views/ViewResume.vue')
    }
  ],
})

export default router
