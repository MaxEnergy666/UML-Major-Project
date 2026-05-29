import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/auth/LoginView.vue'),
      meta: { requiresAuth: false },
    },
    {
      path: '/',
      component: () => import('@/layouts/MainLayout.vue'),
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          name: 'Dashboard',
          component: () => import('@/views/DashboardView.vue'),
        },
        {
          path: 'profile',
          name: 'Profile',
          component: () => import('@/views/profile/ProfileView.vue'),
        },
        {
          path: 'portrait',
          name: 'Portrait',
          component: () => import('@/views/profile/PortraitView.vue'),
        },
        {
          path: 'jobs',
          name: 'Jobs',
          component: () => import('@/views/jobs/JobsView.vue'),
        },
        {
          path: 'career/plan',
          name: 'CareerPlan',
          component: () => import('@/views/career/PlanView.vue'),
        },
        {
          path: 'career/directions',
          name: 'CareerDirections',
          component: () => import('@/views/career/DirectionsView.vue'),
        },
        {
          path: 'career/recommendations',
          name: 'CareerRecommendations',
          component: () => import('@/views/career/RecommendationsView.vue'),
        },
        {
          path: 'career/improvement',
          name: 'CareerImprovement',
          component: () => import('@/views/career/ImprovementView.vue'),
        },
        {
          path: 'career/interview',
          name: 'MockInterview',
          component: () => import('@/views/career/InterviewView.vue'),
        },
        {
          path: 'career/resume',
          name: 'ResumeOptimization',
          component: () => import('@/views/career/ResumeView.vue'),
        },
        {
          path: 'admin/users',
          name: 'AdminUsers',
          component: () => import('@/views/admin/UsersView.vue'),
        },
        {
          path: 'admin/stats',
          name: 'AdminStats',
          component: () => import('@/views/admin/StatsView.vue'),
        },
        {
          path: 'admin/logs',
          name: 'AdminLogs',
          component: () => import('@/views/admin/LogsView.vue'),
        },
      ],
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/login',
    },
  ],
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  if (to.meta.requiresAuth !== false && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.path === '/login' && authStore.isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

export default router
