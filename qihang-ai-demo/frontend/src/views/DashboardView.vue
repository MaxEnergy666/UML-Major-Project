<template>
  <div class="dashboard">
    <!-- 欢迎区域 -->
    <div class="welcome-section">
      <h2>欢迎回来，{{ authStore.user?.name || '同学' }}！</h2>
      <p>今天是你职业规划的新起点</p>
    </div>

    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stat-cards">
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-icon" style="background: #e6f4ff;">
            <el-icon size="28" color="#1677FF"><User /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">INTJ-A</div>
            <div class="stat-label">MBTI 类型</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-icon" style="background: #f6ffed;">
            <el-icon size="28" color="#52C41A"><TrendCharts /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">IAS</div>
            <div class="stat-label">霍兰德代码</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-icon" style="background: #fff7e6;">
            <el-icon size="28" color="#FAAD14"><Star /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">82.5</div>
            <div class="stat-label">综合胜任力</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-icon" style="background: #fff1f0;">
            <el-icon size="28" color="#F5222D"><Briefcase /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">5</div>
            <div class="stat-label">推荐方向</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 主要内容区 -->
    <el-row :gutter="20" class="main-content">
      <!-- 左侧：胜任力雷达图 -->
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>胜任力雷达图</span>
              <el-button type="primary" link @click="$router.push('/portrait')">查看详情</el-button>
            </div>
          </template>
          <div ref="radarChart" style="height: 300px;"></div>
        </el-card>
      </el-col>

      <!-- 右侧：最新规划摘要 -->
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>最新职业规划</span>
              <el-button type="primary" link @click="$router.push('/career/plan')">查看完整规划</el-button>
            </div>
          </template>
          <div class="plan-summary">
            <div class="plan-item">
              <div class="plan-tag short">短期 (0-6月)</div>
              <p>夯实编程基础，掌握 Python/Java 核心技术栈，完成 1-2 个高质量项目，为秋招做准备。</p>
            </div>
            <div class="plan-item">
              <div class="plan-tag mid">中期 (6月-2年)</div>
              <p>进入互联网大厂实习，积累工程实践经验，深入学习 AI/大数据方向技术。</p>
            </div>
            <div class="plan-item">
              <div class="plan-tag long">长期 (2-5年)</div>
              <p>成为 AI 领域技术专家，具备独立负责大型项目的能力，向技术管理方向发展。</p>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 底部区域 -->
    <el-row :gutter="20" class="bottom-content">
      <!-- 推荐岗位 Top 3 -->
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>推荐岗位 Top 3</span>
              <el-button type="primary" link @click="$router.push('/career/recommendations')">查看全部</el-button>
            </div>
          </template>
          <div class="job-list">
            <div v-for="job in topJobs" :key="job.id" class="job-item">
              <div class="job-info">
                <h4>{{ job.title }}</h4>
                <p>{{ job.company }} · {{ job.city }}</p>
              </div>
              <div class="job-match">
                <el-progress type="circle" :percentage="job.match" :width="50" :stroke-width="4" color="#1677FF" />
              </div>
            </div>
          </div>
        </el-card>
      </el-col>

      <!-- 快捷入口 -->
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>
            <span>快捷入口</span>
          </template>
          <div class="quick-links">
            <div class="quick-link" @click="$router.push('/career/interview')">
              <el-icon size="32" color="#1677FF"><Mic /></el-icon>
              <span>模拟面试</span>
            </div>
            <div class="quick-link" @click="$router.push('/career/resume')">
              <el-icon size="32" color="#52C41A"><Document /></el-icon>
              <span>简历优化</span>
            </div>
            <div class="quick-link" @click="$router.push('/career/directions')">
              <el-icon size="32" color="#FAAD14"><Compass /></el-icon>
              <span>方向推荐</span>
            </div>
            <div class="quick-link" @click="$router.push('/career/improvement')">
              <el-icon size="32" color="#F5222D"><DataLine /></el-icon>
              <span>提升建议</span>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { useAuthStore } from '@/stores/auth'
import * as echarts from 'echarts'
import { User, TrendCharts, Star, Briefcase, Mic, Document, Compass, DataLine } from '@element-plus/icons-vue'

const authStore = useAuthStore()
const radarChart = ref<HTMLElement>()

const topJobs = ref([
  { id: 1, title: 'AI 算法工程师', company: '字节跳动', city: '北京', match: 92 },
  { id: 2, title: '数据分析师', company: '阿里巴巴', city: '杭州', match: 87 },
  { id: 3, title: '后端开发工程师', company: '腾讯', city: '深圳', match: 83 },
])

onMounted(() => {
  nextTick(() => {
    if (radarChart.value) {
      const chart = echarts.init(radarChart.value)
      chart.setOption({
        radar: {
          indicator: [
            { name: '学习能力', max: 100 },
            { name: '沟通能力', max: 100 },
            { name: '团队协作', max: 100 },
            { name: '问题解决', max: 100 },
            { name: '领导力', max: 100 },
            { name: '创新能力', max: 100 },
          ],
          radius: '65%',
        },
        series: [{
          type: 'radar',
          data: [{
            value: [85, 70, 78, 82, 65, 88],
            name: '胜任力',
            areaStyle: { color: 'rgba(22, 119, 255, 0.2)' },
            lineStyle: { color: '#1677FF' },
            itemStyle: { color: '#1677FF' },
          }],
        }],
      })
    }
  })
})
</script>

<style scoped>
.dashboard {
  padding: 0;
}

.welcome-section {
  margin-bottom: 24px;
}

.welcome-section h2 {
  margin: 0 0 8px;
  font-size: 24px;
  color: #1d2129;
}

.welcome-section p {
  margin: 0;
  color: #86909c;
}

.stat-cards {
  margin-bottom: 20px;
}

.stat-card {
  display: flex;
  align-items: center;
  padding: 20px;
}

.stat-card :deep(.el-card__body) {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-value {
  font-size: 24px;
  font-weight: 600;
  color: #1d2129;
}

.stat-label {
  font-size: 14px;
  color: #86909c;
  margin-top: 4px;
}

.main-content,
.bottom-content {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.plan-summary {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.plan-item {
  padding: 12px;
  background: #fafafa;
  border-radius: 8px;
}

.plan-tag {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  margin-bottom: 8px;
}

.plan-tag.short {
  background: #e6f4ff;
  color: #1677FF;
}

.plan-tag.mid {
  background: #f6ffed;
  color: #52C41A;
}

.plan-tag.long {
  background: #fff7e6;
  color: #FAAD14;
}

.plan-item p {
  margin: 0;
  font-size: 14px;
  color: #4e5969;
  line-height: 1.6;
}

.job-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.job-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px;
  background: #fafafa;
  border-radius: 8px;
}

.job-info h4 {
  margin: 0 0 4px;
  font-size: 15px;
  color: #1d2129;
}

.job-info p {
  margin: 0;
  font-size: 13px;
  color: #86909c;
}

.quick-links {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.quick-link {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 24px;
  background: #fafafa;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.quick-link:hover {
  background: #e6f4ff;
  transform: translateY(-2px);
}

.quick-link span {
  font-size: 14px;
  color: #4e5969;
}
</style>
