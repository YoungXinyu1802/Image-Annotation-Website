import Vue from 'vue'
import Router from 'vue-router'
import Layout from '../layout'

Vue.use(Router)

/**
 * hidden: true                  如果设置为 true，该项菜单将不会显示在菜单栏中(默认为 false)
 * meta : {
    title: 'title'               菜单名
    icon: 'icon-name'            图标名
    fixed: true                  如果设置为 true，该项 tag 将一直存在 tag 栏中(默认为 false)
  }
 * */

export const constantRoutes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login'),
    hidden: true,
    meta: { title: '登录' }
  },
  {
    path: '/signup',
    name: 'Signup',
    component: () => import('../views/Signup'),
    hidden: true,
    meta: { title: '注册' }
  },
  {
    path: '/',
    name: 'Layout',
    component: Layout,
    redirect: '/home',
    children: [{
      path: 'home',
      name: 'Home',
      component: () => import('../views/Home'),
      meta: {
        title: '首页',
        icon: 'vue-dsn-icon-index',
        fixed: true
      }
    }]
  },
  {
    path: '/',
    name: 'Layout',
    component: Layout,
    redirect: '/tasklist',
    children: [{
      path: 'tasklist',
      name: 'TaskList',
      component: () => import('../views/TaskList'),
      meta: {
        title: '任务列表',
        icon: 'vue-dsn-icon-wendang',
      }
    }]
  },
  {
    path: '/',
    name: 'Layout',
    component: Layout,
    redirect: '/uploadImg',
    children: [{
      path: 'uploadImg',
      name: 'UploadImg',
      component: () => import('../views/UploadImg'),
      meta: {
        title: '图片上传',
        icon: 'vue-dsn-icon-picture',
      }
    }]
  },
  {
    path: '/',
    name: 'Layout',
    component: Layout,
    redirect: '/uploadVideo',
    children: [{
      path: 'uploadVideo',
      name: 'UploadVideo',
      component: () => import('../views/UploadVideo'),
      meta: {
        title: '视频上传',
        icon: 'vue-dsn-icon-video',
      }
    }]
  },


  {
    path: '/',
    name: 'Layout',
    component: Layout,
    redirect: '/createTask',
    children: [{
      path: 'createTask',
      name: 'CreateTask',
      component: () => import('../views/CreateTask'),
      meta: {
        title: '任务创建',
        icon: 'vue-dsn-icon-biaoge',
      }
    }]
  },

  {
    path: '/',
    name: 'Layout',
    component: Layout,
    redirect: '/imgLabel',
    children: [{
      path: 'imgLabel',
      name: 'ImgLabel',
      component: () => import('../views/LabelImg'),
      meta: {
        title: '图片标注',
        icon: 'vue-dsn-icon-bianjiqi',
      }
    }]
  },
  {
    path: '/',
    name: 'Layout',
    component: Layout,
    redirect: '/user-center',
    hidden: true,
    children: [{
      path: 'user-center',
      name: 'UserCenter',
      component: () => import('../views/UserCenter'),
      meta: {
        title: '个人中心'
      }
    }]
  }
]

const routes = [...constantRoutes]

export default new Router({
  routes
})

