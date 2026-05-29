<template>
  <el-container class="layout-container">
    <!-- 左侧导航栏 -->
    <el-aside width="220px" class="aside">
      <div class="logo">
        <h2>启航AI</h2>
        <p>职业生涯规划系统</p>
      </div>
      <el-menu
        :default-active="activeMenu"
        background-color="#001529"
        text-color="#ffffffa6"
        active-text-color="#1677FF"
        @select="handleMenuSelect"
      >
        <el-menu-item index="/">
          <el-icon><HomeFilled /></el-icon>
          <span>首页</span>
        </el-menu-item>

        <el-sub-menu index="user">
          <template #title>
            <el-icon><User /></el-icon>
            <span>个人中心</span>
          </template>
          <el-menu-item index="/profile">基本信息</el-menu-item>
          <el-menu-item index="/portrait">用户画像</el-menu-item>
        </el-sub-menu>

        <el-menu-item index="/jobs">
          <el-icon><Briefcase /></el-icon>
          <span>招聘信息</span>
        </el-menu-item>

        <el-sub-menu index="career">
          <template #title>
            <el-icon><TrendCharts /></el-icon>
            <span>职业生涯规划</span>
          </template>
          <el-menu-item index="/career/plan">职业规划建议</el-menu-item>
          <el-menu-item index="/career/directions">就业方向推荐</el-menu-item>
          <el-menu-item index="/career/recommendations">岗位推荐</el-menu-item>
          <el-menu-item index="/career/improvement">提升建议</el-menu-item>
          <el-menu-item index="/career/interview">模拟面试</el-menu-item>
          <el-menu-item index="/career/resume">简历优化</el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="admin" v-if="authStore.isAdmin">
          <template #title>
            <el-icon><Setting /></el-icon>
            <span>系统管理</span>
          </template>
          <el-menu-item index="/admin/users">用户管理</el-menu-item>
          <el-menu-item index="/admin/stats">数据统计</el-menu-item>
          <el-menu-item index="/admin/logs">系统日志</el-menu-item>
        </el-sub-menu>
      </el-menu>
    </el-aside>

    <!-- 右侧内容区 -->
    <el-container>
      <!-- 顶部栏 -->
      <el-header class="header">
        <div class="header-left">
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item v-if="currentTitle">{{ currentTitle }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        <div class="header-right">
          <el-dropdown @command="handleCommand">
            <span class="user-info">
              <el-avatar :size="32" icon="UserFilled" />
              <span class="username">{{ authStore.user?.name || '用户' }}</span>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">个人信息</el-dropdown-item>
                <el-dropdown-item command="logout" divided>退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <!-- 主内容区 -->
      <el-main class="main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { HomeFilled, User, Briefcase, TrendCharts, Setting } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const activeMenu = computed(() => route.path)

const menuTitles: Record<string, string> = {
  '/': '首页',
  '/profile': '基本信息',
  '/portrait': '用户画像',
  '/jobs': '招聘信息',
  '/career/plan': '职业规划建议',
  '/career/directions': '就业方向推荐',
  '/career/recommendations': '岗位推荐',
  '/career/improvement': '提升建议',
  '/career/interview': '模拟面试',
  '/career/resume': '简历优化',
  '/admin/users': '用户管理',
  '/admin/stats': '数据统计',
  '/admin/logs': '系统日志',
}

const currentTitle = computed(() => menuTitles[route.path] || '')

function handleMenuSelect(index: string) {
  router.push(index)
}

function handleCommand(command: string) {
  if (command === 'profile') {
    router.push('/profile')
  } else if (command === 'logout') {
    authStore.logout()
    router.push('/login')
  }
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
}

.aside {
  background-color: #001529;
  overflow-y: auto;
}

.logo {
  height: 80px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: #fff;
  border-bottom: 1px solid #ffffff1a;
}

.logo h2 {
  margin: 0;
  font-size: 22px;
  color: #1677FF;
}

.logo p {
  margin: 4px 0 0;
  font-size: 12px;
  color: #ffffffa6;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #fff;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
  padding: 0 24px;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  cursor: pointer;
  gap: 8px;
}

.username {
  font-size: 14px;
  color: #333;
}

.main {
  background-color: #f0f2f5;
  padding: 24px;
  overflow-y: auto;
}

/* 子菜单箭头：收起时向右，展开时向下 */
:deep(.el-sub-menu__icon-arrow) {
  transform: rotate(-90deg) !important;
}

:deep(.el-sub-menu.is-opened > .el-sub-menu__title .el-sub-menu__icon-arrow) {
  transform: rotate(0deg) !important;
}
</style>
