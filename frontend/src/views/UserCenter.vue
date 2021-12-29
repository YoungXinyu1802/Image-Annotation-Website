<template>
  <div class="user-center-wrapper clear-fix">
    <el-card shadow="always" :body-style="{padding: '50px'}">
      <img src="../assets/img/Home.png" alt="icon" class="img">
      <el-row class="row">
        <el-col :span="10">
          <div class="user-avatar">
            <img src="../assets/img/avatar.png" alt="avatar">
          </div>
        </el-col>
        <el-col :span="14">
          <el-form label-width="100px">
            <el-form-item label="用户名">
              <el-input :placeholder="this.userInfo.username" :disabled="true" style="width:200px"></el-input>
            </el-form-item>
            <el-form-item label="邮箱">
              <el-input :placeholder="this.userInfo.email" :disabled="true" style="width:200px"></el-input>
            </el-form-item>
          </el-form>
        </el-col>
      </el-row>

    </el-card>
  </div>
</template>

<script>
import { getUserInfo } from '../api/login'

export default {
  name: 'UserCenter',
  data() {
    return {
      userInfo: {
        username: localStorage.getItem('username'),
        email: localStorage.getItem('email')
      }
    }
  },
  created() {
  }
}
</script>

<style lang="less">
.user-center-wrapper {
  .row{
    margin-top: 40px;
  }
  .user-avatar {
    float: right;
    width: 100px;
    height: 100px;
  }
  .user-info {
    float: left;
    width: 800px;
    margin-left: 50px;
    margin-bottom: 50px;
    li {
      height: 34px;
      line-height: 34px;
      label,
      span {
        display: inline-block;
        vertical-align: middle;
      }
      label {
        width: 80px;
        margin-right: 12px;
        text-align: right;
      }
    }
  }
}
</style>
