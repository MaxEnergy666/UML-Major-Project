<template>
  <div class="users-page">
    <div class="page-header">
      <h2>用户管理</h2>
      <p>查看和管理系统用户</p>
    </div>

    <!-- 统计卡片 -->
    <el-row :gutter="16" class="stat-row">
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-num">128</div>
          <div class="stat-label">总用户数</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-num" style="color: #52C41A;">96</div>
          <div class="stat-label">已认证用户</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-num" style="color: #1677FF;">112</div>
          <div class="stat-label">活跃用户</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-num" style="color: #FAAD14;">16</div>
          <div class="stat-label">今日新增</div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 用户列表 -->
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <span>用户列表</span>
          <div class="header-actions">
            <el-input
              v-model="searchText"
              placeholder="搜索用户名/姓名/手机号"
              prefix-icon="Search"
              clearable
              style="width: 260px; margin-right: 12px;"
            />
            <el-select v-model="filterRole" placeholder="角色筛选" clearable style="width: 120px; margin-right: 12px;">
              <el-option label="全部" value="" />
              <el-option label="普通用户" value="student" />
              <el-option label="管理员" value="admin" />
            </el-select>
            <el-select v-model="filterStatus" placeholder="状态筛选" clearable style="width: 120px;">
              <el-option label="全部" value="" />
              <el-option label="已认证" value="verified" />
              <el-option label="未认证" value="unverified" />
            </el-select>
          </div>
        </div>
      </template>

      <el-table :data="filteredUsers" stripe style="width: 100%;">
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="username" label="用户名" width="140" />
        <el-table-column prop="name" label="姓名" width="100" />
        <el-table-column prop="phone" label="手机号" width="130" />
        <el-table-column prop="university" label="学校" width="160" />
        <el-table-column prop="major" label="专业" width="140" />
        <el-table-column label="角色" width="100">
          <template #default="{ row }">
            <el-tag :type="row.role === 'admin' ? 'danger' : 'primary'" size="small">
              {{ row.role === 'admin' ? '管理员' : '普通用户' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="认证状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_verified ? 'success' : 'info'" size="small">
              {{ row.is_verified ? '已认证' : '未认证' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="date_joined" label="注册时间" width="110" />
        <el-table-column label="操作" fixed="right" width="160">
          <template #default>
            <el-button type="primary" link size="small">查看</el-button>
            <el-button type="primary" link size="small">编辑</el-button>
            <el-button type="danger" link size="small">禁用</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-wrap">
        <el-pagination
          v-model:current-page="currentPage"
          :page-size="10"
          :total="128"
          layout="total, prev, pager, next"
          background
        />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const searchText = ref('')
const filterRole = ref('')
const filterStatus = ref('')
const currentPage = ref(1)

// 静态演示数据
const users = ref([
  { id: 1, username: 'demo_student', name: '何家齐', phone: '13800138000', university: '华南理工大学', major: '软件工程', role: 'student', is_verified: true, date_joined: '2026-03-15' },
  { id: 2, username: 'admin', name: '林嘉明', phone: '13800138001', university: '-', major: '-', role: 'admin', is_verified: true, date_joined: '2026-01-01' },
  { id: 3, username: 'chenyuxin', name: '陈雨欣', phone: '13912568723', university: '北京大学', major: '计算机科学与技术', role: 'student', is_verified: true, date_joined: '2026-03-20' },
  { id: 4, username: 'huangzitao', name: '黄子韬', phone: '13678234591', university: '清华大学', major: '人工智能', role: 'student', is_verified: true, date_joined: '2026-03-22' },
  { id: 5, username: 'linxiaowan', name: '林小婉', phone: '15899342167', university: '浙江大学', major: '数据科学与大数据技术', role: 'student', is_verified: false, date_joined: '2026-04-01' },
  { id: 6, username: 'wangjunhao', name: '王俊豪', phone: '18266349012', university: '复旦大学', major: '软件工程', role: 'student', is_verified: true, date_joined: '2026-04-05' },
  { id: 7, username: 'zhouyutong', name: '周雨桐', phone: '13755489023', university: '上海交通大学', major: '信息安全', role: 'student', is_verified: true, date_joined: '2026-04-08' },
  { id: 8, username: 'liuhanyu', name: '刘瀚宇', phone: '15933672845', university: '南京大学', major: '电子信息工程', role: 'student', is_verified: false, date_joined: '2026-04-10' },
  { id: 9, username: 'xujiayi', name: '徐嘉怡', phone: '18644129087', university: '华中科技大学', major: '通信工程', role: 'student', is_verified: true, date_joined: '2026-04-12' },
  { id: 10, username: 'zhangmingxuan', name: '张明轩', phone: '13399876541', university: '武汉大学', major: '人工智能', role: 'student', is_verified: true, date_joined: '2026-04-15' },
  { id: 11, username: 'wenzixin', name: '温子欣', phone: '15077689234', university: '中山大学', major: '软件工程', role: 'student', is_verified: true, date_joined: '2026-04-18' },
  { id: 12, username: 'gaoyichen', name: '高逸尘', phone: '17822345698', university: '哈尔滨工业大学', major: '计算机科学与技术', role: 'student', is_verified: false, date_joined: '2026-04-20' },
])

const filteredUsers = computed(() => {
  return users.value.filter(u => {
    const matchSearch = !searchText.value ||
      u.username.includes(searchText.value) ||
      u.name.includes(searchText.value) ||
      u.phone.includes(searchText.value)
    const matchRole = !filterRole.value || u.role === filterRole.value
    const matchStatus = !filterStatus.value ||
      (filterStatus.value === 'verified' && u.is_verified) ||
      (filterStatus.value === 'unverified' && !u.is_verified)
    return matchSearch && matchRole && matchStatus
  })
})
</script>

<style scoped>
.users-page {
  padding: 0;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0 0 4px;
  font-size: 20px;
  color: #1d2129;
}

.page-header p {
  margin: 0;
  font-size: 14px;
  color: #86909c;
}

.stat-row {
  margin-bottom: 20px;
}

.stat-card :deep(.el-card__body) {
  text-align: center;
  padding: 20px;
}

.stat-num {
  font-size: 28px;
  font-weight: 600;
  color: #1d2129;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 13px;
  color: #86909c;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 16px;
  font-weight: 600;
}

.header-actions {
  display: flex;
  align-items: center;
}

.pagination-wrap {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
}
</style>
